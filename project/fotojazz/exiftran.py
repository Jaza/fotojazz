#!./bin/python

from subprocess import Popen, PIPE

from project.fotojazz.fotojazzprocess import FotoJazzProcess, FotoJazzProcessShellRun


class ExifTranProcess(FotoJazzProcess):
    def run(self):
        """Invokes exiftran on the command line, and reads each line of its shell output until it's finished execution. This process effectively halts further progress of the program, which is why it's contained in a thread. Continuously updates the value of files_processed_count."""
        self.prepare_filenames()
        cmd = 'exiftran -aip %s' % self.filenames_str
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


if __name__ == '__main__':
    FotoJazzProcessShellRun(ExifTranProcess)()
