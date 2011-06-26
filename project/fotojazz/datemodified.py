#!./bin/python

from glob import glob
from os import path, utime
from threading import Thread
import sys
from time import mktime, sleep

import pyexiv2

from project.fotojazz.fotojazzprocess import FotoJazzProcess, FotoJazzProcessShellRun


class DateModifiedProcess(FotoJazzProcess):
    def run(self):
        """Changes the date modified to match the Exif date taken, for all images in the specified file path."""
        self.prepare_filenames()
        
        for filename in self.filenames:
            metadata = pyexiv2.ImageMetadata(filename)
            metadata.read()
            date_taken = metadata['Exif.Photo.DateTimeOriginal'].value
            date_taken_timestamp = int(mktime(date_taken.timetuple()))
            utime(filename, (date_taken_timestamp, date_taken_timestamp))
            self.files_processed_count += 1


if __name__ == '__main__':
    FotoJazzProcessShellRun(DateModifiedProcess)()    
