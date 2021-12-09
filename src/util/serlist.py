import bisect
import pickle

class AbstractSerializableList(object):
    '''
        A serializable list
        
        Usage: inherit class and set file_path to valid file to store list in
    '''
    list = []
    loaded = False
    file_path = None

    @classmethod
    def insert(cls, i, item):
        '''
            qFile:  QuarantinedFile object
        '''
        cls.list.insert(i, item)
        
    @classmethod
    def remove(cls, item):
        '''
            qFile:  QuarantinedFile object
        '''
        if (item in cls.list):
            cls.list.remove(item)

    @classmethod
    def find(cls, item):
        '''
            Return True if item is in list, else returns False
        '''
        if(item in cls.list):
            return True
        else:
            return False

    @classmethod
    def save(cls):
        with open(cls.file_path, "wb") as file:
            pickle.dump(cls.list, file)

    @classmethod
    def load(cls):
        if (not cls.loaded):
            try:
                with open(cls.file_path, "rb") as file:
                    cls.list = pickle.load(file)
                    cls.loaded = True
            except FileNotFoundError:
                pass 
    @classmethod
    def get(cls, index):
        return cls.list[index]
    
    @classmethod
    def len(cls):
        return len(cls.list)

    @classmethod
    def bisect_insort(cls, item):
        bisect.insort(cls.list, item)
    
    @classmethod
    def index(cls, item):
        return cls.list.index(item)
