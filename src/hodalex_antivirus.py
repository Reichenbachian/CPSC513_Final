import click
import config
import os
from pathlib import Path
from scanner import SignatureScanner, RegexScanner

def run_folder_scan(folder):
	scanner = SignatureScanner(config.SIGNATURE_FILE)
	for root, dirs, files in os.walk(folder):
		for file in files:
			path = os.path.join(root, file)
			if Path(path).is_file():
				is_virus, virus_info = scanner.scan_file(path)
				if is_virus:
					print(f"Found a virus at {path}")

@click.command()
@click.option('--scan', 'scan_folder', help='Scan a specific folder.')
def main(scan_folder):
	if scan_folder is not None:
		run_folder_scan(scan_folder)

if __name__ == "__main__":
	main()