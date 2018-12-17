![grail.png](/icon/grailkit.png)


# Grail Kit #

Grailkit is a library for creative and experimental coding. This library used for development of Grail application (http://grailapp.com).
Grailkit includes handling of Project, CueList's, Cue and reading/writing to *.grail files.
Reading and writing to grail bible format. Implements MIDI, OSC, DMX protocols.
 
## Modules and features ##

**Core:**

* db - Thin sqlite database wrapper
* core - Signals and basic types
* plug - Plugin loading/registration
* util - Utility functions, constants and classes

**Grail file format:**

* dna - Grail format I/O
* bible - Grail bible format I/O
* bible_parse - Parsing other bible formats to grail format

**Protocols & communication:**

* osc - Open Sound Control protocol in pure python
* dmx - DMX I/O based on RS245 (experimental)
* midi - MIDI I/O library

## Requirements ##

Python 3.3+

This library is in Pure Python and depends only on following projects:

* python-rtmidi (MIDI module)
* pyserial (DMX module)
* pybind11
