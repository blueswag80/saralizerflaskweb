from zipfile import ZipFile, is_zipfile
import os
from os import listdir
from shutil import rmtree

class SarZipFile(object):
    
    def __init__(self, zfile):
        self.zfile = ZipFile(zfile)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zfile.close()

    def unzip(self, path):
        self.zfile.extractall(path)

    def check_uncompressed_size(self):
        zinfo = self.zfile.infolist()
        total = 0

        for item in zinfo:
            total = total + item.file_size
        
        return total

        return zinfo.file_size()

    @staticmethod
    def check_is_zipfile(zfile):
        return is_zipfile(zfile)


class SarFile(object):
    def __init__(self, sfile, path):
        self.sfile = sfile
        self.path = path
    
    def get_contents(self):
        with open(os.path.join(self.path, self.sfile), 'r') as infile:
            return infile.read().splitlines()


def list_sar_logs(path):
    return listdir(path)


def remove_sar_logs(path):
    try:
        rmtree(path)
        return True

    except OSError:
        return False


def setup_upload_directory(path):
        if os.path.isdir(path):
            return
        os.mkdir(path)
        # apparently python 3.0 requires the 0o for octals
        os.chmod(path, 0o0755)
        return