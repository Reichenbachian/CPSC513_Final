import config
from util.serlist import AbstractSerializableList

class QFileList(AbstractSerializableList):
    '''
        A serializable list of quantine file metadata
    '''
    file_path = config.QFILE_LIST_FILE
