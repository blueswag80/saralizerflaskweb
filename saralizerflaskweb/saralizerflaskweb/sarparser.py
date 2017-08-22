import re as rexpression

class sarparser(object):
    """description of class"""
    def __init__(self, sarfile):
        self.sarfile = sarfile

    def analyzeSarLog(self):
        saritems = []
        for line in self.sarfile.getContents():          
            if "Average:" in line:
                return saritems

            tokenline = rexpression.split("\s+", line)

            if len(tokenline) < 12 or not "all" in tokenline:
                continue

            saritems.append(tokenline)

        return None
