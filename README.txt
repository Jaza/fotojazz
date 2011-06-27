FotoJazz
========

A tool for cleaning up your photo collection.

- Rotates an image to its correct orientation, per its Exif metadata.
- Shifts the Exif 'date taken' value of an image backwards or forwards by a specified time interval.
- Renames a batch of images per a specified prefix, and with a unique integer ID.
- Updates the 'date modified' metadata of an image to match its 'take taken' value.

Requirements:

- Python 2.6+
- Flask 0.6.1 (will install automatically if you use pip install with the provided requirements.txt file)
- pyexiv2 0.3.0 <http://tilloy.net/dev/pyexiv2/> (the project home page has Windows installers, Debian / Ubuntu / Fedora package details, and - failing that - source packages)

Recommended:

- virtualenv
- pip
- JS-enabled browser (front-end tested on latest Firefox and Chrome)

Instructions:

1. Web-based

- Start the server by opening a terminal window and typing:
  ./runserver.py /path/to/photos/
  Where '/path/to/photos/' is the path to a directory containing jpg photos that you want to work with.

- In a browser, go to:
  http://localhost:5000/

- You can change the file browser path in the 'path to folder' text box. The photo listing area will refresh via AJAX whenever you change the path.

- Select the photos that you want to work with (by default all are selected).

- To fix orientation of images, just push the button and wait for the progress bar to finish.

- To shift the date taken, in the 'shift date by' text box, enter a time interval in the format:
  [-][Xhr][Xm][Xs]
  E.g. to shift dates forward by 3 hours and 30 seconds, enter:
  3hr30s
  Or to shift dates back by 23 minutes, enter:
  -23m
  Then push the button and wait for the progress bar to finish.

- To rename files with unique ID, in the 'give renamed files the prefix' text box, enter a prefix, e.g:
  new_york_trip_may2008
  Then push the button and wait for the progress bar to finish.
  Say you're working on 11 photos, they'll be renamed to:
  new_york_trip_may2008_01.jpg
  new_york_trip_may2008_02.jpg
  new_york_trip_may2008_03.jpg
  new_york_trip_may2008_04.jpg
  new_york_trip_may2008_05.jpg
  new_york_trip_may2008_06.jpg
  new_york_trip_may2008_07.jpg
  new_york_trip_may2008_08.jpg
  new_york_trip_may2008_09.jpg
  new_york_trip_may2008_10.jpg
  new_york_trip_may2008_11.jpg
  The unique ID is padded with leading zeros, as needed per the batch.

- To fix the date modified, just push the button and wait for the progress bar to finish. This will also fix the date created, date accessed, and Exif 'PhotoDate' (which might be different to the Exif 'PhotoDateOriginal', which is the authoritative 'date taken' field).

2. Command line

- To fix the orientation of images, run:
  ./project/fotojazz/exiftran.py /path/to/photos/

- To shift the date taken of images, run:
  ./project/fotojazz/shiftdate.py /path/to/photos/ [-][Xhr][Xm][Xs]
  E.g. to shift dates forward by 3 hours and 30 seconds, enter:
  ./project/fotojazz/shiftdate.py /path/to/photos/ 3hr30s

- To rename images with unique ID, run:
  ./project/fotojazz/renamewithid.py /path/to/photos/ your_prefix

- To fix the date modified of images, run:
  ./project/fotojazz/datemodified.py /path/to/photos/

- For all these command-line tools, progress indication will be output once per second.

- Also, for all of them, all images in the specified directory will be processed.

- Warning: all these tools begin immediately upon execution, there is no 'are you sure' prompt.

========

Created by Jeremy Epstein <http://greenash.net.au/>. Use it as you will: hack, fork, play. 
