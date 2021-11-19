import os


SIGNATURE_FILE = "../db/virus_signatures.csv"


## Resolve relative paths
SIGNATURE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), SIGNATURE_FILE))
