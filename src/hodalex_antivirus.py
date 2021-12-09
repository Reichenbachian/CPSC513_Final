import click
import config
from scanner import SCANNERS
from counter_measures import CounterMeasures

def run_folder_scan(folder):
	counter_measures = CounterMeasures(config.QUARANTINE_FOLDER)
	for scanner in SCANNERS:
		for virus, virus_info in scanner.scan_folder(folder):
			counter_measures.address_virus(virus, virus_info)


@click.command()
@click.option('--scan', 'scan_folder', help='Scan a specific folder.')
def main(scan_folder):
	if scan_folder is not None:
		run_folder_scan(scan_folder)

if __name__ == "__main__":
	main()