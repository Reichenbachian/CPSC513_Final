import os

import config
from datetime import datetime
from util.serlist import AbstractSerializableList

class QFileList(AbstractSerializableList):
    '''
        A serializable list of quarantine file metadata
    '''
    list = []
    file_path = config.QFILE_LIST_FILE
    last_mod = datetime.now()

    @classmethod
    def load(cls):
        super().load()
        if (not cls._sanity_check()):
            cls.list = []
            super().save()

    @classmethod
    def _sanity_check(cls):
        q_folder_len = len([qfile for qfile in os.listdir(config.QUARANTINE_FOLDER) if os.path.isfile(qfile)])
        return len(cls.list) == q_folder_len
        
class AllowList(AbstractSerializableList):
    '''
        A serializable list of file paths that the antivirus will ignore
    '''
    list = []
    file_path = config.ALLOW_LIST_FILE
    last_mod = datetime.now()

    @classmethod
    def insert(cls, i, item):
        item = item.replace('/', os.sep).replace('\\', os.sep)
        return super().insert(i, item)
    
    @classmethod
    def bisect_insort(cls, item):
        item = item.replace('/', os.sep).replace('\\', os.sep)
        return super().bisect_insort(item)
    
    @classmethod
    def index(cls, item):
        item = item.replace('/', os.sep).replace('\\', os.sep)
        return super().index(item)
    
    @classmethod
    def find(cls, item):
        item = item.replace('/', os.sep).replace('\\', os.sep)
        return super().find(item)
    
    @classmethod
    def remove(cls, item):
        item = item.replace('/', os.sep).replace('\\', os.sep)
        return super().remove(item)

class ScanScheduleList(AbstractSerializableList):
    '''
        A serializable list of scan schedules
    '''
    list = []
    file_path = config.SCAN_SCHED_FILE
    last_mod = datetime.now()
