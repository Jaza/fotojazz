import Image
from os import path


def add_trailing_slash(filepath):
    '''Adds a trailing slash to a filepath, if it doesn't already
    have one.'''
    suffix = '/'
    if filepath.endswith('/'):
        suffix = ''
    return '%s%s' % (filepath, suffix)


def get_thumb_metadata(filename, thumb_resize_width, thumb_resize_height):
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
    
    return {'filename': path.basename(filename),
            'fullname': filename,
            'thumb_width': int(thumb_width),
            'thumb_height': int(thumb_height),
            'top_offset': top_offset,
            'left_offset': left_offset}

