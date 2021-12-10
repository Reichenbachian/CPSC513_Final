# Hodalex AntiVirus

## Testing Command
```
python scripts/create_virus_folder.py -t test_regex -t test_static_hash -t test_chunk_hash; python src/hodalex_antivirus.py --scan /tmp/virus/; cat /tmp/virus_scanner.log
```

## Requirements
 - Python 3.9
 - pyqt5
 - pyqt5-tools
 - numpy
 - pandas

## Given Project Description
 - Scan for files containing malware signatures (hashes and binary regex)
	- Scheduled
	- Before a file is executed
 - Configurable countermeasures
	- Remove
	- Isolate (cannot be executed/copied/moved)
	- Warn
 - GUI to manage allowlist, scanning, and signatures
 - Only inside a VM

## Skeletal Design
 - final/
	 - ui/resources/
	 - util/
	 - db/
		- virus_signature.csv
		- virus_regex.csv
 	 - src/
 	 	- scanner.py
 	 	- gui.py
 	 	- counter_measures.py
 	 	- hodalex_antivirus.py

## Initial Timeline
 - Nov 19, Have skeleton code of scanner.py working with given signatures
 - Nov 29, Have first draft GUI (80% done)
 - Nov 29, Finish scanning code (including syscall stuff if that's a thing)
 - Dec 2, Have countermeasures done
 - Dec 5, Robust testing
 - Dec 10, Be done
