import re as rexpression

class SarParser(object):
    """description of class"""
    def __init__(self, sarfile):
        self.sarfile = sarfile
        self.location = 0

    def analyze_sar_log(self):
        sardata = {}
        sarcontents = self.sarfile.get_Contents()

        sardata['cpuinfo'] = self.analyze_cpuinfo(sarcontents)
        sardata['memoryinfo'] = self.analyze_meminfo(sarcontents[self.location:])
        return sardata

    def analyze_cpuinfo(self,sarcontents):
        saritems = []
        for i, line in enumerate(sarcontents):
            if "Average:" in line:
                self.location = i
                return saritems

            tokenline = rexpression.split("\s+", line)

            if len(tokenline) < 12 or not "all" in tokenline:
                continue

            saritems.append(tokenline)
        return None

    def analyze_meminfo(self, sarcontents):
        saritems = []
        startparse = False
        for i, line in enumerate(sarcontents):
            # We need to see this line to know we are in the correct spot
            if 'kbmemfree' in line:
                startparse = True
                continue

            # If we have not found the start point keep looking
            if not startparse:
                continue

            if startparse is True and 'Average' in line:
                self.location = self.location + i
                return saritems

            saritems.append(rexpression.split("\s+", line))
