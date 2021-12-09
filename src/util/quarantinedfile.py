import config

from datetime import datetime
from util.serlist import AbstractSerializableList

class QuarantinedFile(object):
    '''
        Object for quarantined file management

        Attributes:
            name [String]: name of file
            dir [String]: the former location of the quarantined file
            old_perm [String]: permissions before file was quarantined
            time [datetime]: the time at which file was quarantined
    
    '''
    def __init__(self, name, path, perm, time):
        self.name = name
        self.path = path
        self.time = time    #daytime object
        self.old_perm = perm
    
    def __str__(self):
        return f"{self.path} | {self.time.hour:02}:{self.time.minute:02}:{self.time.second:02}"
    
    def __repr__(self):
        return self.__str__()
    
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

class QFileList(AbstractSerializableList):
    '''
        A serializable list of quantine file metadata
    '''
    file_path = config.QFILE_LIST_FILE