from datetime import datetime
from PIL import Image
from os import path, stat
import pyexiv2
from stat import ST_MTIME, ST_SIZE
from time import mktime


def add_trailing_slash(filepath):
    '''Adds a trailing slash to a filepath, if it doesn't already
    have one.'''
    suffix = '/'
    if filepath.endswith('/'):
        suffix = ''
    return '%s%s' % (filepath, suffix)


def get_thumb_metadata(filename, thumb_resize_width, thumb_resize_height, checked=True):
    '''For the given image and its requested thumbnail size, returns
    a dictionary of metadata needed to display the image as a
    thumbnail.'''

    img = Image.open(filename)
    width, height = img.size
    ratio = 1.0 * width / height
    thumb_width = thumb_resize_width
    thumb_height = thumb_resize_height
    top_offset = 0
    left_offset = 0

    if ratio > 1.0:
        thumb_width = thumb_resize_width
        thumb_height = thumb_resize_height * (1.0 / ratio)
        top_offset = int((thumb_resize_height - thumb_height) / 2)
    elif ratio < 1.0:
        thumb_width = thumb_resize_width * ratio
        thumb_height = thumb_resize_height
        left_offset = int((thumb_resize_width - thumb_width) / 2)

    statinfo = stat(filename)

    metadata = pyexiv2.ImageMetadata(filename)
    metadata.read()
    date_taken = metadata['Exif.Photo.DateTimeOriginal'].value
    orientation = metadata['Exif.Image.Orientation'].value

    return {'fullname': filename,
            'thumb_width': int(thumb_width),
            'thumb_height': int(thumb_height),
            'top_offset': top_offset,
            'left_offset': left_offset,
            'checked': checked,
            'filename': path.basename(filename),
            'filesize': statinfo[ST_SIZE],
            'date_taken_timestamp': mktime(date_taken.timetuple()),
            'date_taken': date_taken,
            'date_modified_timestamp': statinfo[ST_MTIME],
            'date_modified': datetime.fromtimestamp(statinfo[ST_MTIME]),
            'orientation': orientation}
