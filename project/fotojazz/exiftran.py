from glob import glob
from subprocess import Popen, PIPE
from threading import Thread
from time import sleep


class ExifTran(Thread):
    """Calls the command-line exiftran utility within a thread, and
    streams its shell output (which is one line for each file
    processed). Calling code can then monitor the progress of ExifTran
    from outside the thread."""
    
    cmd_with_placeholders = 'exiftran -aip %s'
    filenames_str = ''
    filenames = []
    total_file_count = 0
    
    # This number is updated continuously as the thread runs.
    # Check the value of this number to determine the current progress
    # of exiftran (if it equals 0, progress is 0%; if it equals
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
    
    """Invokes exiftran on the command line, and reads each line of its
    shell output until it's finished execution. This process effectively
    halts further progress of the program, which is why it's contained
    in a thread. Continuously updates the value of
    files_processed_count."""
    def run(self):
        self.prepare_filenames()
        cmd = self.cmd_with_placeholders % self.filenames_str
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).stderr
        
        while 1:
            line = p.readline()
            if not line: break
            # Unfortunately, exiftran dumps progress info as well as
            # error and other messages to stderr. So, we just inspect
            # each line manually: if it begins with 'processing ',
            # it's the latest progress update; otherwise, it's an error
            # or some other message, and we ignore it.
            if line.startswith('processing '): self.files_processed_count += 1
    
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


def exiftran_test_run():
    """Example / test of running an ExifTran instance, and of monitoring
    its progress from outside the thread."""
    
    filenames_input = glob('/home/jaza/tempphotos_testing/*.[jJ][pP]?[gG]')

    et = ExifTran(filenames_input)

    print '%d files' % et.total_file_count
    print et.get_progress()

    et.start()

    while et.is_alive() and et.files_processed_count < et.total_file_count:
        sleep(1)
        if et.files_processed_count < et.total_file_count:
            print et.get_progress()

    if et.files_processed_count == et.total_file_count:
        print et.get_progress()


if __name__ == '__main__':
    exiftran_test_run()    
