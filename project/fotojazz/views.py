from glob import glob
import Image
import os
import sys

from flask import current_app as app
from flask import Module
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
from werkzeug.exceptions import NotFound

from project.library.resize import resize


mod = Module(__name__, 'fotojazz')

@mod.route('/')
def home():
    filebrowse_path = ''
    resize_width = 100
    resize_height = 100
    
    if len(sys.argv) > 1:
        filebrowse_path = sys.argv[1]
        filebrowse_path = '%s%s' % (filebrowse_path,
                                    filebrowse_path.endswith('/') and '' or '/')
    
    filebrowse_files = []
    filebrowse_error = ''
    if not os.path.isdir(filebrowse_path):
        filebrowse_error = 'Specified path is not a valid directory.'
    else:
        glob_pattern = '%s%s' % (filebrowse_path,
                                   '*.[jJ][pP]*[gG]')
        filenames =  glob(glob_pattern)
        for filename in filenames:
            fp = open(filename, 'rb')
            img = Image.open(fp)
            img.load()
            width, height = img.size
            fp.close()
            ratio = 1.0 * width / height
            if ratio > 1.0:
                new_width = resize_width
                new_height = resize_height * (1.0 / ratio)
            elif ratio < 1.0:
                new_width = resize_width * ratio
                new_height = resize_height
            else:
                new_width = resize_width
                new_height = resize_height
            filebrowse_files.append({'filename': os.path.basename(filename),
                                     'fullname': filename,
                                     'width': new_width,
                                     'height': new_height})
        
        if not filebrowse_files:
            filebrowse_error = 'No images in specified directory.'
        else:
            filebrowse_files.sort()
    
    return render_template('home.html', filebrowse_path=filebrowse_path,
                                        filebrowse_error=filebrowse_error,
                                        filebrowse_files=filebrowse_files,
                                        resize_width=resize_width,
                                        resize_height=resize_height)


@mod.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


# Code borrowed from:
# http://flask.pocoo.org/mailinglist/ \
# archive/2011/1/26/pil-to-create-thumbnails- \
# automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7
@mod.route("/thumb")
def thumb():
    file = request.args.get('file', None)
    
    if not file:
        raise NotFound()
    
    width = request.args.get('width', 100)
    height = request.args.get('height', 100)
    quality = request.args.get('quality', 75)
    crop = request.args.get('crop', False)

    out = resize(file=file,
                 width=width,
                 height=height,
                 crop=crop,
                 quality=quality)

    response = Response(mimetype='image/jpeg')
    response.data = out.getvalue()
    return response
