import re as rexpression

class SarParser(object):
    """description of class"""
    def __init__(self, sarfile):
        self.sarfile = sarfile

    def analyze_Sar_Log(self):
        return analyze_cpuinfo()
    
    def analyze_cpuinfo():
        saritems = []
        for line in self.sarfile.getContents():          
            if "Average:" in line:
                return saritems

            tokenline = rexpression.split("\s+", line)

            if len(tokenline) < 12 or not "all" in tokenline:
                continue

            saritems.append(tokenline)
        return None