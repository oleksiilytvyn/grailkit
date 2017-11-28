.. coding=utf-8
.. image:: https://bitbucket.org/repo/nnn7Mr/images/2544725897-grail-kit.png
   :height: 200px
   :width: 200px
   :scale: 100%
   :alt: grailkit

Grail Kit
=========

Grailkit is a library for creative and experimental coding. This library used for development of Grail application (http://grailapp.com).
Grailkit includes handling of Project, CueList's, Cue and reading/writing to *.grail files.
Reading and writing to grail bible format. Implements MIDI, OSC, DMX protocols.

Modules and features
--------------------

Core:

* db - Thin sqlite database wrapper
* core - Signals and basic types
* plug - Plugin loading/registration
* util - Utility functions, constants and classes

Grail file format:

* dna - Grail format I/O
* bible - Grail bible format I/O
* bible_parse - Parsing other bible formats to grail format

Protocols & communication:

* osc - Open Sound Control protocol in pure python
* dmx - DMX I/O based on RS245 (experimental)
* midi - MIDI I/O library


Requirements
------------

This library is in Pure Python and depends only on following projects:

* python-rtmidi (MIDI module)
* pyserial (DMX module)
