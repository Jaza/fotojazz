#!./bin/python

from glob import glob
from os import path, utime
from threading import Thread
import sys
from time import mktime, sleep

import pyexiv2


class DateModified(Thread):
    filenames = []
    filenames_str = ''
    total_file_count = 0
    
    # This number is updated continuously as the thread runs.
    # Check the value of this number to determine the current progress
    # of DateModified (if it equals 0, progress is 0%; if it equals
    # total_file_count, progress is 100%).
    files_processed_count = 0
    
    """When initialising this class, you can pass in either a list of
    filenames (first param), or a string of space-delimited filenames
    (second param). No need to pass in both."""
    def __init__(self, filenames=[], filenames_str=''):
        Thread.__init__(self)
        self.filenames = filenames
        self.filenames_str = filenames_str
        self.prepare_filenames()
        self.files_processed_count = 0
    
    """Changes the date modified to match the Exif date taken, for all
    images in the specified file path. This process effectively
    halts further progress of the program, which is why it's contained
    in a thread. Continuously updates the value of
    files_processed_count."""
    def run(self):
        self.prepare_filenames()
        
        for filename in self.filenames:
            metadata = pyexiv2.ImageMetadata(filename)
            metadata.read()
            date_taken = metadata['Exif.Photo.DateTimeOriginal'].value
            date_taken_timestamp = int(mktime(date_taken.timetuple()))
            utime(filename, (date_taken_timestamp, date_taken_timestamp))
            self.files_processed_count += 1
    
    """Prepares the string and the list of filenames - this is always
    run before the thread begins."""
    def prepare_filenames(self):
        if self.filenames_str != '':
            self.filenames = [x.strip() for x in self.filenames_str.split(' ') if x != '']
            self.total_file_count = len(self.filenames)
        if len(self.filenames):
            self.filenames.sort()
            self.filenames_str = ' '.join(self.filenames)
            self.total_file_count = len(self.filenames)
    
    """Can be called at any time before, during or after thread
    execution, to get current progress."""
    def get_progress(self):
        percent_done = float(self.files_processed_count) / float(self.total_file_count) * 100.0
        return '%d files (%.2f%%)' % (self.files_processed_count, percent_done)


def datemodified_test_run():
    """Example / test of running a DateModified instance, and of monitoring
    its progress from outside the thread."""
    
    if not len(sys.argv) > 1:
        print 'Error: no file path specified.'
        exit()
    
    filebrowse_path = sys.argv[1]
    suffix = '/'
    if filebrowse_path.endswith('/'):
        suffix = ''
    filebrowse_path = '%s%s' % (filebrowse_path,
                                suffix)
    
    if not path.isdir(filebrowse_path):
        print 'Error: invalid file path.'
        exit()
    
    filenames_input = glob('%s*.[jJ][pP]*[gG]' % filebrowse_path)
    
    if not filenames_input:
        print 'Error: no matching files in specified path.'
        exit()

    dm = DateModified(filenames_input)

    print '%d files' % dm.total_file_count
    print dm.get_progress()

    dm.start()

    while dm.is_alive() and dm.files_processed_count < dm.total_file_count:
        sleep(1)
        if dm.files_processed_count < dm.total_file_count:
            print dm.get_progress()

    if dm.files_processed_count == dm.total_file_count:
        print dm.get_progress()


if __name__ == '__main__':
    datemodified_test_run()    
