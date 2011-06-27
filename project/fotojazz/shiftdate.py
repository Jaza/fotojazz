#!./bin/python

import pyexiv2
import sys

from project.library.parsetimedelta import parsetimedelta
from project.fotojazz.fotojazzprocess import FotoJazzProcess, FotoJazzProcessShellRun


class ShiftDateProcess(FotoJazzProcess):
    offset = ''
    
    def __init__(self, *args, **kwargs):
        FotoJazzProcess.__init__(self, *args, **kwargs)
        self.offset = args[0]
    
    def run(self):
        """Shifts the exif date taken by the specified offset, for all images in the specified file path."""
        self.prepare_filenames()
        
        delta = parsetimedelta(self.offset)
        
        for filename in self.filenames:
            metadata = pyexiv2.ImageMetadata(filename)
            metadata.read()
            metadata['Exif.Photo.DateTimeOriginal'].value += delta
            metadata.write()
            self.files_processed_count += 1


if __name__ == '__main__':
    if not len(sys.argv) > 2:
        print 'Error: no time offset string specified.'
        exit()
    FotoJazzProcessShellRun(ShiftDateProcess)(sys.argv[2])
