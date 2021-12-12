import os
import threading
import click
import config
import time
from scanner import SCANNERS
from counter_measures import CounterMeasures
import numpy as np
from PyQt5.QtWidgets import QApplication, QFrame, QMainWindow
from gui import GUI
from virus_info import VirusSeverity
from datetime import datetime
from util.quarantinedfile import QuarantinedFile
from util.datalists import AllowList, QFileList, ScanScheduleList


def run_folder_scan(folder):
	counter_measures = CounterMeasures(config.QUARANTINE_FOLDER)
	for scanner in SCANNERS:
		for virus, virus_info in scanner.scan_folder(folder):
			if (not AllowList.find(virus)):
				if np.any(virus_info == VirusSeverity.QUARANTINE):
					perm = oct(os.stat(virus).st_mode)
					qfile = QuarantinedFile(os.path.basename(virus), virus, perm, datetime.now())
					QFileList.insert(0, qfile)
				counter_measures.address_virus(virus, virus_info)

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

def serialize_lists():
	QFileList.save()
	AllowList.save()
	ScanScheduleList.save()

def background_service():
	scan_folder = config.TEST_VIRUS_DIRECTORY
	ScanScheduleList.load()
	while(True):
		if (ScanScheduleList.len() > 0):
			next = ScanScheduleList.get(0)
			next.wait()
			ScanScheduleList.remove(next)
			if (next.next_schedule()):
				ScanScheduleList.bisect_insort(next)
			bg_scan = threading.Thread(target=run_folder_scan, args=[scan_folder])
			bg_scan.start()
			bg_scan.join()
		time.sleep(2)

@click.command()
@click.option('-s', '--scan', 'scan_folder', type=str, help='Scan a specific folder.')
@click.option('-g', '--gui/--no-gui', 'gui', help='Scan a specific folder.')
def main(scan_folder, gui, bg = None):

	if scan_folder is not None:
		run_folder_scan()
		serialize_lists()
	elif gui:
		bg_scan = threading.Thread(target=background_service)
		bg_scan.setDaemon(True)
		bg_scan.start()
		app = QApplication([])
		app.aboutToQuit.connect(serialize_lists)
		window = QMainWindow()
		g = GUI(window)
		window.show()
		app.exec()
	else:
		print_help()
	

if __name__ == "__main__":
	main()