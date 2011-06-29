#!/usr/bin/env python

from os import utime
from time import mktime

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
            metadata['Exif.Image.DateTime'].value = date_taken
            metadata.write()
            date_taken_timestamp = int(mktime(date_taken.timetuple()))
            utime(filename, (date_taken_timestamp, date_taken_timestamp))
            self.files_processed_count += 1


if __name__ == '__main__':
    FotoJazzProcessShellRun(DateModifiedProcess)()    
