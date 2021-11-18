# Hodalex AntiVirus

## Questions
 - Does nmtui count as a GUI interface?
 - Is there a specific place to get a signature list?
 - ^ same question for binary regex
 - "Before a file is executed" - before any file? Or a list of specific ones? Hijack syscall? Through loader(linker?) ?


## To-Do
 - @alexr Scan for files containing malware signatures (hashes and binary regex)
 - Configurable countermeasures
 - @danielhodeta GUI to manage allowlist, scanning, and signatures

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

## Design
 - final/
	 - db/
		- virus_signature.csv
		- virus_regex.csv
 	 - src/
 	 	- scanner.py
 	 	- gui.py
 	 	- counter_measures.py
 	 	- hodalex_antivirus.py

## Timeline
 - Nov 19, Have skeleton code of scanner.py working with given signatures
 - Nov 29, Have first draft GUI (80% done)
 - Nov 29, Finish scanning code (including syscall stuff if that's a thing)
 - Dec 2, Have countermeasures done
 - Dec 5, Robust testing
 - Dec 10, Be done
