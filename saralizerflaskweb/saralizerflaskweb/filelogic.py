from zipfile import ZipFile
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


    def checkUncompressedSize(self):
        zinfo = self.zfile.infolist()
        total = 0

        for item in zinfo:
            total = total + item.file_size
        
        return total

        return zinfo.file_size()

class SarFile(object):
    def __init__(self, sfile, path):
        self.sfile = sfile
        self.path = path
    
    def getContents(self):
        with open(os.path.join(self.path, self.sfile), 'r') as infile:
            return infile.read().splitlines()

@staticmethod
def checkZipFile(self, zfile):
    return zipfile.is_zipfile(zfile)

def listsarlogs(path):
    return listdir(path)

