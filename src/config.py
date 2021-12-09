import logging
import os


## Signature Files
STATIC_HASH_FILE = "../db/static_signatures.csv"
CHUNK_HASH_FILE = "../db/chunk_signatures.csv"
REGEX_FILE = "../db/regex_signatures.csv"

##Data
DATA_FOLDER = "../data"
QFILE_LIST_FILE = "../data/qfiles"
ALLOW_LIST_FILE = "../data/allowlist"
SCAN_SCHED_FILE = "../data/scansched"

## Options
QUARANTINE_FOLDER = '/tmp/quarantine'
CHUNK_SIZE = 2048

## Test options
TEST_VIRUS_DIRECTORY = "/tmp/virus"
MIN_LENGTH = 0
MAX_LENGTH = 4096
DIRECTORY_CREATION_PCT = 0.1

## Create Logger
LOG_DIRECTORY = '/tmp/virus_scanner.log'
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename=LOG_DIRECTORY, format=FORMAT)
logger = logging.getLogger('antivirus')
logger.setLevel(logging.DEBUG)

## Resolve relative paths
STATIC_HASH_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), STATIC_HASH_FILE))
CHUNK_HASH_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), CHUNK_HASH_FILE))
REGEX_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), REGEX_FILE))
QUARANTINE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), QUARANTINE_FOLDER))
TEST_VIRUS_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), TEST_VIRUS_DIRECTORY))
DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), DATA_FOLDER))
QFILE_LIST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), QFILE_LIST_FILE))
ALLOW_LIST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), ALLOW_LIST_FILE))
SCAN_SCHED_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), SCAN_SCHED_FILE))

## Create folders
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
