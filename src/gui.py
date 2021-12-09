from util.scanschedule import ScanSchedule
from scanner import SCANNERS
from counter_measures import CounterMeasures

from util.guisetup import GUISetup

class GUI(GUISetup):

    def __init__(self, main_window):
        super().__init__(main_window)
        
    def updateProgressBar(self, new_val):
        '''
            Updates the progress bar with some value for nice visuals
        '''
        self.progressBar.setProperty("value", new_val)
    
    def getFilePaths(self):
        '''
            Returns the filepaths the user has selected to scan
        '''
        return self.scan_file_paths
    
    def displayError(self, message):
        '''
            Generic error/warning display function
        '''
        super()._displayError(message)
    
    def getSchedule(self):
        '''
            Returns scan schedule
        '''
        return self.scan_schedule
    
    def addQuarantinedFile(self, qfile):
        '''
            Add file to vault

            Idiom: self.addQuarantinedFile(QuarantinedFile(os.path.basename(file), file, datetime.now()))
        '''
        super().addQuarantinedFile(qfile)
    
    def start_scan(self):
        '''
            This function connects the GUI with the backend

            Potentially useful function:
                getFilePaths: returns
        '''
        pass

