from glob import glob
from os import path
import sys
from uuid import uuid4

from flask import current_app as app
from flask import jsonify
from flask import Module
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
from werkzeug.exceptions import NotFound

from project import fotojazz_processes
from project.library.resize import resize

from exiftran import ExifTran
from utils import add_trailing_slash, get_thumb_metadata


mod = Module(__name__, 'fotojazz')

@mod.route('/')
def home():
    filebrowse_path = ''
    thumb_resize_width = app.config['THUMB_RESIZE_WIDTH']
    thumb_resize_height = app.config['THUMB_RESIZE_HEIGHT']
    filebrowse_files = []
    filebrowse_error = ''
    
    if not len(sys.argv) > 1:
        filebrowse_error = 'No path specified.'
    else:
        filebrowse_path = add_trailing_slash(sys.argv[1])
    
        if not path.isdir(filebrowse_path):
            filebrowse_error = 'Specified path is not a valid directory.'
        else:
            glob_pattern = '%s%s' % (filebrowse_path, '*.[jJ][pP]*[gG]')
            filebrowse_files = [get_thumb_metadata(filename,
                                                   thumb_resize_width,
                                                   thumb_resize_height)
                                for filename in glob(glob_pattern)]
            
            if not filebrowse_files:
                filebrowse_error = 'No images in specified directory.'
            else:
                filebrowse_files.sort()
    
    return render_template('home.html', filebrowse_path=filebrowse_path,
                                        filebrowse_error=filebrowse_error,
                                        filebrowse_files=filebrowse_files,
                                        thumb_resize_width=thumb_resize_width,
                                        thumb_resize_height=thumb_resize_height)


@mod.route('/reorient/start/')
def reorient_start():
    filenames_input = request.args.get('filenames_input', '', type=str)
    et = ExifTran(filenames_str=filenames_input)
    et.start()
    
    if not 'reorient' in fotojazz_processes:
        fotojazz_processes['reorient'] = {}
    key = str(uuid4())
    fotojazz_processes['reorient'][key] = et
    percent_done = round(et.percent_done(), 1)
    done=False
    
    return jsonify(key=key, percent=percent_done, done=done)


@mod.route('/reorient/progress/')
def reorient_progress():
    key = request.args.get('key', '', type=str)
    
    if not 'reorient' in fotojazz_processes:
        fotojazz_processes['reorient'] = {}
    
    if not key in fotojazz_processes['reorient']:
        return jsonify(error='Invalid process key.')
    
    percent_done = fotojazz_processes['reorient'][key].percent_done()
    done = False
    if not fotojazz_processes['reorient'][key].is_alive() or percent_done == 100.0:
        del fotojazz_processes['reorient'][key]
        done = True
    percent_done = round(percent_done, 1)
    
    return jsonify(key=key, percent=percent_done, done=done)


@mod.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@mod.route("/thumb/")
def thumb():
    '''Code borrowed (with modifications) from:
    http://flask.pocoo.org/mailinglist/ \
    archive/2011/1/26/pil-to-create-thumbnails- \
    automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7'''
    
    file = request.args.get('file', None)
    
    if not file:
        raise NotFound()
    
    width = request.args.get('width', app.config['THUMB_RESIZE_WIDTH'], type=int)
    height = request.args.get('height', app.config['THUMB_RESIZE_HEIGHT'], type=int)
    quality = int(request.args.get('quality', 75))
    crop = request.args.get('crop', False)

    out = resize(file=file,
                 width=width,
                 height=height,
                 crop=crop,
                 quality=quality)

    response = Response(mimetype='image/jpeg')
    response.data = out.getvalue()
    return response
