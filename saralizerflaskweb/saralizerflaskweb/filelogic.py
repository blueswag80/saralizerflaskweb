from zipfile import ZipFile, is_zipfile
import os
from os import listdir

class SarZipFile(object):
    
    def __init__(self, zfile):
        self.zfile = ZipFile(zfile)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zfile.close()


    def unzip(self, path):
        self.zfile.extractall(path)


    def check_Uncompressed_Size(self):
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
    
    def get_Contents(self):
        with open(os.path.join(self.path, self.sfile), 'r') as infile:
            return infile.read().splitlines()

def list_sar_logs(path):
    return listdir(path)

