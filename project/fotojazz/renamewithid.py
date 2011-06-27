#!./bin/python

from os import rename
import sys

from project.library.parsetimedelta import parsetimedelta
from project.fotojazz.fotojazzprocess import FotoJazzProcess, FotoJazzProcessShellRun


class RenameWithIdProcess(FotoJazzProcess):
    prefix = ''
    
    def __init__(self, *args, **kwargs):
        FotoJazzProcess.__init__(self, *args, **kwargs)
        self.prefix = args[0]
    
    def run(self):
        """Renames file with prefix and a unique incremented integer ID, for all images in the specified file path."""
        self.prepare_filenames()
        
        fill = len(str(self.total_file_count))
        
        for filename in self.filenames:
            new_filename = '%s%s_%0*d.jpg' % (self.filebrowse_path, self.prefix, fill, self.files_processed_count+1)
            rename(filename, new_filename)
            self.files_processed_count += 1


if __name__ == '__main__':
    if not len(sys.argv) > 2:
        print 'Error: no rename prefix string specified.'
        exit()
    FotoJazzProcessShellRun(RenameWithIdProcess)(sys.argv[2])
