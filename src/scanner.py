import hashlib
import numpy as np

class Scanner(object):
	'''
	This is the abstract class
	'''

	def scan_file(self, file):
		'''
		Returns:
			- True/False: If a virus has been detected
			- Dict: If the first item is true, it returns a dict with
					virus information. 
		'''
		raise NotImplementedError()


class SignatureScanner(Scanner):
	'''
	The signature scanner does md5 hashes of files and compares
	them against a signature list.
	'''
	def __init__(self, signature_folder):
		super().__init__()
		self.signatures = np.array([x.strip() for x in open(signature_folder).readlines()])

	def scan_file(self, file):
		file_contents = open(file, 'rb').read()
		file_hash = hashlib.md5(file_contents).hexdigest()
		return np.any(self.signatures == file_hash), {}


class RegexScanner(Scanner):
	'''
	The regex scanner does string matching in order
	to find viruses and implements a version of the Scanner
	abstract class.
	'''
	def __init__(self, regex_folder):
		super().__init__()
		self.signatures = open(regex_folder).readlines()


	def scan_file(self, file):
		pass
