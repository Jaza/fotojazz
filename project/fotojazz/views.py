from glob import glob
from operator import itemgetter
from os import path
import sys
import time
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

from utils import add_trailing_slash, get_thumb_metadata


mod = Module(__name__, 'fotojazz')


@mod.route('/')
def home():
    """Displays the FotoJazz home page."""
    
    filebrowse_path = ''
    if len(sys.argv) > 1:
        filebrowse_path = add_trailing_slash(sys.argv[1])
    
    # The filebrowse area has to be rendered by a separate function,
    # becase it's refreshed via AJAX.
    filebrowse_files_rendered = photos(filebrowse_path, check_all=True)
    
    return render_template('home.html', filebrowse_path=filebrowse_path,
           filebrowse_files_rendered=filebrowse_files_rendered)


@mod.route('/process/start/<process_class_name>/')
def process_start(process_class_name):
    """Starts the specified threaded process. This is a sort-of
    'generic' view, all the different FotoJazz tasks share it.
    
    This view expects the following GET parameters:
    - filenames_input: string-delimited list of absolute paths of
      photo files to process.
    - filebrowse_path: absolute path to current browsing directory.
    - extra_args: semicolon-delimited extra args, for any extra info
      that certain tasks may need (e.g. rename prefix).
    
    Returns a JSON object with these attrs:
    - key: unique ID for the process that has just been started. This
           is needed in order to query the progress of the process via
           the AJAX process_progress() view.
    - percent: percent of the process done (always 0, it just started).
    - done: boolean indicating if the process is done (always 0, it
            just started)."""
    
    filenames_input = request.args.get('filenames_input', '', type=str)
    process_module_name = process_class_name
    if process_class_name != 'FotoJazzProcess':
        process_module_name = process_module_name.replace('Process', '')
    process_module_name = process_module_name.lower()
    
    # Dynamically import the class / module for the particular process
    # being started. This saves needing to import all possible
    # modules / classes.
    process_module_obj = __import__('%s.%s.%s' % ('project',
                                                  'fotojazz',
                                                  process_module_name),
                                    fromlist=[process_class_name])
    process_class_obj = getattr(process_module_obj, process_class_name)
    
    args = []
    filebrowse_path = request.args.get('filebrowse_path', '', type=str)
    extra_args_input = request.args.get('extra_args', '', type=str)
    if extra_args_input != '':
        args = extra_args_input.split(';')
    kwargs = {
        'filenames_str': filenames_input,
        'filebrowse_path': filebrowse_path
    }
    
    # Initialise the process thread object.
    fjp = process_class_obj(*args, **kwargs)
    fjp.start()
    
    if not process_class_name in fotojazz_processes:
        fotojazz_processes[process_class_name] = {}
    key = str(uuid4())
    
    # Store the process thread object in a global dict variable, so it
    # continues to run and can have its progress queried, independent
    # of the current session or the current request.
    fotojazz_processes[process_class_name][key] = fjp
    
    percent_done = round(fjp.percent_done(), 1)
    done=False
    
    return jsonify(key=key, percent=percent_done, done=done)


@mod.route('/process/progress/<process_class_name>/')
def process_progress(process_class_name):
    """Reports on the progress of the specified threaded process.
    This is a sort-of 'generic' view, all the different FotoJazz tasks
    share it.
    
    This view expects the following GET parameters:
    - key: unique ID for the process to be reported on, as returned by
           the AJAX process_start() view.
    
    Returns a JSON object with these attrs:
    - key: unique ID for the process being reported on.
    - percent: percent of the process done.
    - done: boolean indicating if the process is done."""
    
    key = request.args.get('key', '', type=str)
    
    if not process_class_name in fotojazz_processes:
        fotojazz_processes[process_class_name] = {}
    
    if not key in fotojazz_processes[process_class_name]:
        return jsonify(error='Invalid process key.')
    
    # Retrieve progress of requested process thread, from global
    # dict variable where the thread reference is stored.
    percent_done = fotojazz_processes[process_class_name][key] \
                   .percent_done()
    
    done = False
    if not fotojazz_processes[process_class_name][key].is_alive() or \
       percent_done == 100.0:
        del fotojazz_processes[process_class_name][key]
        done = True
    percent_done = round(percent_done, 1)
    
    return jsonify(key=key, percent=percent_done, done=done)


@mod.route('/favicon.ico')
def favicon():
    """Renders the favicon."""
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico')


@mod.route('/photos/')
def photos(photos_path='', check_all=False):
    """Renders the photo browsing block. This view is often called by
    AJAX, as this block gets refreshed dynamically.
    
    This view expects the following GET params:
    - filenames_input: space-delimited string of absolute paths to
                       the photos that should be rendered with their
                       checkbox checked by default.
    - check_all: boolean indicating if all photos should be rendered
                 with their checkbox checked by default. If true,
                 filenames_input is ignored.
    - photos_path: absolute path to the directory from which to load
                   photos."""
    
    filenames_str = request.args.get('filenames_input', '', type=str)
    filenames_input = []
    if filenames_str != '':
        filenames_input = [x.strip() for x in filenames_str.split(' ')
                                     if x != '']
    if len(filenames_input):
        filenames_input.sort()
    check_all_arg = request.args.get('check_all', '', type=str)
    if check_all_arg != '':
        check_all = int(check_all_arg) and True or False
    filebrowse_files = []
    filebrowse_path = ''
    filebrowse_error = ''
    
    if not photos_path:
        photos_path = request.args.get('photos_path', '', type=str)
    
    if not photos_path:
        filebrowse_error = 'No path specified.'
    else:
        filebrowse_path = add_trailing_slash(photos_path)
    
    thumb_resize_width = app.config['THUMB_RESIZE_WIDTH']
    thumb_resize_height = app.config['THUMB_RESIZE_HEIGHT']
    
    if not path.isdir(filebrowse_path):
        filebrowse_error = 'Specified path is not a valid directory.'
    else:
        glob_pattern = '%s%s' % (filebrowse_path, '*.[jJ][pP]*[gG]')
        filenames = glob(glob_pattern)
        filebrowse_files = [get_thumb_metadata(
                            filename,
                            thumb_resize_width,
                            thumb_resize_height,
                            checked=check_all or
                            filename in filenames_input)
                            for filename in filenames]
        
        if not filebrowse_files:
            filebrowse_error = 'No images in specified directory.'
        else:
            filebrowse_files.sort(
            key=itemgetter('date_taken_timestamp'))
    
    # Need to add timestamp to thumbnail img src's, as a unique url
    # value to ensure fresh thumbs get shown on ajax refresh. Doesn't
    # actually need to be passed as a get param to '/thumbs/' (although
    # it does get passed), not used for anything else.
    timestamp = int(time.time())
    return render_template('fragments/photos.html',
                           filebrowse_files=filebrowse_files,
                           filenames_input=filenames_input,
                           filebrowse_error=filebrowse_error,
                           thumb_resize_width=thumb_resize_width,
                           thumb_resize_height=thumb_resize_height,
                           timestamp=timestamp)


@mod.route("/thumb/")
def thumb():
    '''Code borrowed (with modifications) from:
    http://flask.pocoo.org/mailinglist/ \
    archive/2011/1/26/pil-to-create-thumbnails- \
    automatically-using-tag/#32aff91e05ba9985a49a76a4fb5338d7'''
    
    file = request.args.get('file', None)
    
    if not file:
        raise NotFound()
    
    width = request.args.get('width',
                             app.config['THUMB_RESIZE_WIDTH'],
                             type=int)
    height = request.args.get('height',
                              app.config['THUMB_RESIZE_HEIGHT'],
                              type=int)
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
