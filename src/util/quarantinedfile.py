from datetime import datetime

class QuarantinedFile(object):
    '''
        Object for quarantined file management

        Attributes:
            name [String]: name of file
            dir [String]: the former location of the quarantined file
            time [datetime]: the time at which file was quarantined
    
    '''
    def __init__(self, name, dir, time):
        self.name = name
        self.dir = dir
        self.time = time    #daytime object
    
    def __str__(self):
        return f"{self.dir} | {self.time.hour():02}:{self.time.minute():02}:{self.time.second():02}"
    
    def __repr__(self):
        self.__str__()
    
    def __eq__(self, other):
        if (self.time == other.time):
            return True
        else:
            return False
    
    def __lt__(self, other):
        if (self.time < other.time):
            return True
        else:
            return False