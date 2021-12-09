import os
import pickle
import config

from datetime import datetime

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

class QFileList(object):
    '''
        A serializable list of quantine file metadata
    '''
    qfile_list = []
    loaded = False

    @classmethod
    def insert(cls, i, qFile):
        '''
            qFile:  QuarantinedFile object
        '''
        cls.qfile_list.insert(i, qFile)
        
    @classmethod
    def remove(cls, qFile):
        '''
            qFile:  QuarantinedFile object
        '''
        if (qFile in cls.qfile_list):
            cls.qfile_list.remove(qFile)

    @classmethod
    def save(cls):
        with open(config.QFILE_LIST_FILE, "wb") as qfile:
            pickle.dump(cls.qfile_list, qfile)

    @classmethod
    def load(cls):
        if (not cls.loaded):
            try:
                with open(config.QFILE_LIST_FILE, "rb") as qfile:
                    cls.qfile_list = pickle.load(qfile)
                    cls.loaded = True
            except FileNotFoundError:
                pass 
    @classmethod
    def get(cls, index):
        return cls.qfile_list[index]