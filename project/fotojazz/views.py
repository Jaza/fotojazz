from glob import glob
import os
import sys

from flask import current_app as app
from flask import Module
from flask import render_template
from flask import send_from_directory

from project.library import resize


mod = Module(__name__, 'fotojazz')

@mod.route('/')
def home():
    filebrowse_path = ''
    if len(sys.argv) > 1:
        filebrowse_path = sys.argv[1]
    
    filebrowse_files = []
    filebrowse_error = ''
    if not os.path.isdir(filebrowse_path):
        filebrowse_error = 'Specified path is not a valid directory.'
    else:
        glob_pattern = '%s%s%s' % (filebrowse_path,
                                   filebrowse_path.endswith('/') and '' or '/',
                                   '*.[jJ][pP]*[gG]')
        print glob_pattern
        filebrowse_files = glob(glob_pattern)
        if not filebrowse_files:
            filebrowse_error = 'No images in specified directory.'
    
    return render_template('home.html', filebrowse_path=filebrowse_path,
                                        filebrowse_error=filebrowse_error)

@mod.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


# Code borrowed from:
# http://flask.pocoo.org/mailinglist/ \
# archive/2011/1/26/pil-to-create-thumbnails- \
# automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7
@mod.route("/thumbs")
def thumbs():
    # not good (type of values) but something like this
    file = request.args.get('file', None)
    width = request.args.get('width', 120)
    height = request.args.get('height', 90)
    quality = request.args.get('height', 70)
    crop = request.args.get('crop', False)

    # image
    img = Image.open(file)
    newpath = ""
    out = file(newpath, "w")
    resize(img, (width, height), crop, out, quality)

    return send_file(out)
