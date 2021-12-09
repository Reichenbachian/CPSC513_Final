import os

from config import logger
from virus_info import VirusSeverity

class CounterMeasures():
	def __init__(self, quarantine_folder):
		self.quarantine_folder = quarantine_folder

	def address_virus(self, fp, virus_info):
		severity = virus_info['severity']
		if severity == VirusSeverity.WARN:
			self.warn_file(fp)
		elif severity == VirusSeverity.QUARANTINE:
			self.quarantine_file(fp)
		elif severity == VirusSeverity.DELETE:
			self.remove_file(fp)

	def quarantine_file(self, file):
		logger.warning(f"A virus has been detected in the file {file}. It is being quarantined.")
		new_path = os.path.join(self.quarantine_folder, os.path.basename(file))
		os.rename(file, new_path)
		os.chmod(new_path, 0o444)

	def remove_file(self, file):
		logger.warning(f"A virus has been detected in the file {file}. It is being removed.")
		os.remove(file)

	def warn_file(self, file):
		logger.warning(f"A virus has been detected in the file {file}.")
