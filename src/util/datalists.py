import config
from util.serlist import AbstractSerializableList

class QFileList(AbstractSerializableList):
    '''
        A serializable list of quarantine file metadata
    '''
    list = []
    file_path = config.QFILE_LIST_FILE

class AllowList(AbstractSerializableList):
    '''
        A serializable list of file paths that the antivirus will ignore
    '''
    list = []
    file_path = config.ALLOW_LIST_FILE

class ScanScheduleList(AbstractSerializableList):
    '''
        A serializable list of scan schedules
    '''
    list = []
    file_path = config.SCAN_SCHED_FILE
