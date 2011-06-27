#!./bin/python

from glob import glob
import sys
from subprocess import Popen, PIPE
from threading import Thread
from time import sleep


class FotoJazzProcess(Thread):
    """Parent / example class for running threaded FotoJazz processes. You should use this as a base class if you want to process a directory full of files, in batch, within a thread, and you want to report on the progress of the thread."""
    
    filenames_str = ''
    filebrowse_path = ''
    filenames = []
    total_file_count = 0
    
    # This number is updated continuously as the thread runs.
    # Check the value of this number to determine the current progress
    # of FotoJazzProcess (if it equals 0, progress is 0%; if it equals
    # total_file_count, progress is 100%).
    files_processed_count = 0
    
    def __init__(self, *args, **kwargs):
        """When initialising this class, you can pass in either a list of filenames (first param), or a string of space-delimited filenames (second param). No need to pass in both."""
        Thread.__init__(self)
        if 'filenames' in kwargs:
            self.filenames = kwargs['filenames']
        if 'filenames_str' in kwargs:
            self.filenames_str = kwargs['filenames_str']
        self.filebrowse_path = kwargs['filebrowse_path']
        self.prepare_filenames()
        self.files_processed_count = 0
    
    def run(self):
        """Iterates through the files in the specified directory. This example implementation just sleeps on each file - in subclass implementations, you should do some real processing on each file (e.g. re-orient the image, change date modified). You should also generally call self.prepare_filenames() at the start, and increment self.files_processed_count, in subclass implementations."""
        self.prepare_filenames()
        
        for filename in self.filenames:
            sleep(0.1)
            self.files_processed_count += 1
    
    def prepare_filenames(self):
        """Prepares the string and the list of filenames - this is always run before the thread begins."""
        if self.filenames_str != '':
            self.filenames = [x.strip() for x in self.filenames_str.split(' ') if x != '']
            self.total_file_count = len(self.filenames)
        if len(self.filenames):
            self.filenames.sort()
            self.filenames_str = ' '.join(self.filenames)
            self.total_file_count = len(self.filenames)
    
    def percent_done(self):
        """Gets the current percent done for the thread."""
        return float(self.files_processed_count) / float(self.total_file_count) * 100.0
    
    def get_progress(self):
        """Can be called at any time before, during or after thread execution, to get current progress."""
        return '%d files (%.2f%%)' % (self.files_processed_count, self.percent_done())


class FotoJazzProcessShellRun():
    """Runs an instance of the thread with shell output / feedback."""
    
    def __init__(self, init_class=FotoJazzProcess):
        self.init_class = init_class
    
    def __call__(self, *args, **kwargs):
        if not len(sys.argv) > 1:
            print 'Error: no file path specified.'
            exit()
        
        filebrowse_path = sys.argv[1]
        suffix = '/'
        if filebrowse_path.endswith('/'):
            suffix = ''
        filebrowse_path = '%s%s' % (filebrowse_path,
                                    suffix)
        filenames_input = glob('%s*.[jJ][pP]*[gG]' % filebrowse_path)
        kwargs['filenames'] = filenames_input
        kwargs['filebrowse_path'] = filebrowse_path
        fjp = self.init_class(*args, **kwargs)

        print '%s threaded process beginning.' % fjp.__class__.__name__
        print '%d files will be processed. Now beginning progress output.' % fjp.total_file_count
        print fjp.get_progress()

        fjp.start()

        while fjp.is_alive() and fjp.files_processed_count < fjp.total_file_count:
            sleep(1)
            if fjp.files_processed_count < fjp.total_file_count:
                print fjp.get_progress()

        if fjp.files_processed_count == fjp.total_file_count:
            print fjp.get_progress()
            print '%s threaded process complete. Now exiting.' % fjp.__class__.__name__


if __name__ == '__main__':
    FotoJazzProcessShellRun()()
