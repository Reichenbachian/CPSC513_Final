import os
import click
import hashlib
import random
import sys
import uuid

## Add src to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")))
import config

### Helper Functions

def create_chunk_of_length(length):
	s = ""
	for i in range(length):
		s += chr(random.randint(0, 0x110000))
	return s

def create_random_file(fp):
	length = random.randint(config.MIN_LENGTH, config.MAX_LENGTH)
	s = create_chunk_of_length(length)
	with open(fp, 'wb') as f:
		f.write(s.encode(errors='ignore'))

def create_file_name(out_dir):
	## Sometimes create a new subdirectory to test
	## directory crawling
	if random.random() < config.DIRECTORY_CREATION_PCT:
		new_outdir = os.path.join(out_dir, str(uuid.uuid4()))
		os.makedirs(new_outdir)
		return create_file_name(new_outdir)
	return os.path.join(out_dir, str(uuid.uuid4()))

### Tests
def test_static_hash():
	'''
	This test is designed to test the static hash scanner.
	'''
	random_files = random.randint(0, 30)
	test_fp = os.path.join(config.TEST_VIRUS_DIRECTORY, str(uuid.uuid4()))
	
	## Write virus file
	contents = "VIRUS_CONTENTS"
	with open(test_fp, 'wb') as f:
		f.write(contents.encode(errors='ignore'))

	## Write random files
	for i in range(random_files):
		fp = create_file_name(config.TEST_VIRUS_DIRECTORY)
		create_random_file(fp)

def test_chunk_hash():
	'''
	This test is designed to test the chunked hash scanner

	'''
	random_files = random.randint(0, 30)
	test_fp = os.path.join(config.TEST_VIRUS_DIRECTORY, str(uuid.uuid4()))
	
	## Write virus file
	contents = "VIRUS_CONTENTS"
	contents += "A"*(config.CHUNK_SIZE - len(contents))
	contents += create_chunk_of_length(random.randint(0, 2048))

	with open(test_fp, 'wb') as f:
		f.write(contents.encode(errors='ignore'))

	## Write random files
	for i in range(random_files):
		fp = create_file_name(config.TEST_VIRUS_DIRECTORY)
		create_random_file(fp)

def test_regex():
	'''
	This test is designed to test the chunked hash scanner

	'''
	random_files = random.randint(0, 30)
	test_fp = os.path.join(config.TEST_VIRUS_DIRECTORY, str(uuid.uuid4()))
	
	## Write virus file
	contents = create_chunk_of_length(random.randint(0, 2048))
	contents += "VIRUS_CONTENTS"
	contents += create_chunk_of_length(random.randint(0, 2048))

	with open(test_fp, 'wb') as f:
		f.write(contents.encode(errors='ignore'))

	## Write random files
	for i in range(random_files):
		fp = create_file_name(config.TEST_VIRUS_DIRECTORY)
		create_random_file(fp)


TESTS = {
			"test_static_hash": test_static_hash,
		 	"test_chunk_hash": test_chunk_hash,
		 	"test_regex": test_regex
		 }

@click.command()
@click.option('-t', '--test_name', 'test_names', type=str, multiple=True)
def main(test_names):
	for name in test_names:
		os.makedirs(config.TEST_VIRUS_DIRECTORY, exist_ok=True)
		TESTS[name]()

if __name__ == "__main__":
	main()