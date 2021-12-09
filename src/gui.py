import os
from util.quarantinedfile import QuarantinedFile, QFileList
from util.scanschedule import ScanSchedule
from scanner import SCANNERS

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

    def updateVault(self):
        '''
            Updates the vault entries based on the current list of QuarantinedFiles
        '''
        super()._updateVault()
    
    def start_scan(self):
        '''
            This function connects the GUI with the backend

            Potentially useful functions:
                getFilePaths: returns a list of strings, each a file path
                displayError: display an error dialog with some message
                updateProgressBar: nice UI for user to see progress of scan
        '''
        pass

