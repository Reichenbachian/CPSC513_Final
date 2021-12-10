import os
import config
import logging
import numpy as np
from util.quarantinedfile import QuarantinedFile
from util.datalists import QFileList
from scanner import SCANNERS
from counter_measures import CounterMeasures
from virus_info import VirusSeverity
from util.datalists import AllowList, QFileList
from datetime import datetime

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
    
    def displayMessage(self, message):
        '''
            Generic error/warning display function
        '''
        super()._displayMessage(message)

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
        folders = self.getFilePaths()
        if folders == None or len(folders) <= 0:
            return
        total_cpts = len(folders) * len(SCANNERS)
        detected = 0
        #total_cpts = 0
        # for folder in folders:
        #     total_cpts += sum(len(files) for _,_,files in os.walk(folder))
        progress_markers = [round(x/total_cpts*100, 1) for x in range(1,total_cpts+1,1)]
        cpt = 0
        counter_measures = CounterMeasures(config.QUARANTINE_FOLDER)
        for folder in folders:
            for scanner in SCANNERS:
                for virus, virus_info in scanner.scan_folder(folder):
                    if (not AllowList.find(virus)):
                        if np.any(virus_info == VirusSeverity.QUARANTINE):
                            perm = oct(os.stat(virus).st_mode)
                            qfile = QuarantinedFile(os.path.basename(virus), virus, perm, datetime.now())
                            QFileList.insert(0, qfile)
                        counter_measures.address_virus(virus, virus_info)
                        detected += 1
                self.updateProgressBar(progress_markers[cpt])
                cpt = min(total_cpts-1, cpt+1)

        if (detected > 0):
            self.displayMessage(f"Scanning complete. Detected {detected} malware files! See {config.LOG_DIRECTORY} for details.")
        else:
            self.displayMessage("Scanning complete! No malware detected!")
        self.updateProgressBar(0)

