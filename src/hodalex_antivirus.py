import os
import click
import config
from scanner import SCANNERS
from counter_measures import CounterMeasures
from PyQt5.QtWidgets import QApplication, QFrame, QMainWindow
from gui import GUI
from virus_info import VirusSeverity
from datetime import datetime
from util.quarantinedfile import QuarantinedFile, QFileList


def run_folder_scan(folder):
	counter_measures = CounterMeasures(config.QUARANTINE_FOLDER)
	for scanner in SCANNERS:
		for virus, virus_info in scanner.scan_folder(folder):
			if (virus_info == VirusSeverity.QUARANTINE):
				perm = oct(os.stat(virus).st_mode)
				qfile = QuarantinedFile(os.path.basename(virus), virus, perm, datetime.now())
				QFileList.insert(0, qfile)
			counter_measures.address_virus(virus, virus_info)

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

@click.command()
@click.option('-s', '--scan', 'scan_folder', type=str, help='Scan a specific folder.')
@click.option('-g', '--gui/--no-gui', 'gui', help='Scan a specific folder.')
def main(scan_folder, gui):
	if scan_folder is not None:
		run_folder_scan(scan_folder)
	elif gui:
		app = QApplication([])
		window = QMainWindow()
		g = GUI(window)
		window.show()
		app.exec()
	else:
		print_help()

if __name__ == "__main__":
	main()