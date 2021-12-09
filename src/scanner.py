import config
import hashlib
import numpy as np
import os
from pathlib import Path
import pandas as pd
import re

class Scanner(object):
	'''
	This is the abstract class
	'''

	def scan_folder(self, folder):
		for root, dirs, files in os.walk(folder):
			for file in files:
				path = os.path.join(root, file)
				if Path(path).is_file():
					is_virus, virus_info = self.scan_file(path)
					if is_virus:
						yield path, virus_info

	def scan_file(self, file):
		'''
		Returns:
			- True/False: If a virus has been detected
			- Dict: If the first item is true, it returns a dict with
					virus information. 
		'''
		raise NotImplementedError()


class ChunkHashScanner(Scanner):
	def __init__(self, signature_file, chunk_size=2048):
		self.signatures = pd.read_csv(signature_file)
		self.chunk_size = chunk_size

	def scan_file(self, file):
		f = open(file, 'rb')
		chunk = f.read(self.chunk_size)
		while chunk:
			file_hash = hashlib.md5(chunk).hexdigest()
			mask = file_hash == self.signatures['signature']
			if np.any(mask):
				idx = np.argmax(mask)
				return True, self.signatures.iloc[idx]
			chunk = f.read(self.chunk_size)

		return False, {}


class HashScanner(Scanner):
	'''
	The signature scanner does md5 hashes of files and compares
	them against a signature list.
	'''
	def __init__(self, signature_folder):
		super().__init__()
		self.signatures = pd.read_csv(signature_folder)

	def scan_file(self, file):
		file_contents = open(file, 'rb').read()
		file_hash = hashlib.md5(file_contents).hexdigest()

		mask = self.signatures == file_hash
		return np.any(mask), self.signatures.iloc[np.argmax(mask)]


class RegexScanner(Scanner):
	'''
	The regex scanner does string matching in order
	to find viruses and implements a version of the Scanner
	abstract class.
	'''
	def __init__(self, signature_folder):
		super().__init__()
		self.signatures = pd.read_csv(signature_folder)


	def scan_file(self, file):
		contents = open(file, 'rb').read()
		for i, signature in enumerate(self.signatures['signature']):
			if len(re.findall(signature.encode(), contents)) > 0:
				return True, self.signatures.iloc[i]
		return False, {}


SCANNERS = [
			ChunkHashScanner(config.CHUNK_HASH_FILE),
			HashScanner(config.STATIC_HASH_FILE),
			RegexScanner(config.REGEX_FILE)
		   ]

