
.. image:: https://bitbucket.org/repo/nnn7Mr/images/2544725897-grail-kit.png
   :height: 200px
   :width: 200px
   :scale: 100%
   :alt: grailkit

Grail Kit
=========

Grailkit is a standard library for development of Grail application.
Grailkit includes handling of Project, CueList's, Cue and reading/writing to *.grail files.
Reading and writing to grail bible format.
Also grailkit implements new PyQt5 widgets and dialogs.

Modules and features:

* db - sqlite database wrapper
* osc - Open Sound Control in pure python
* dna - grail format I/O
* dmx - DMX I/O based on RS245
* core - Signals and basic types
* midi - live MIDI playback
* plug - plugin loading/registration
* util - utility functions and constants
* bible - grail bible format I/O
* bible_parse - parsing bible formats to grail format

Requirements
------------

This library is Pure Python and depends on following other projects:

* PyQt (Qt components)
* pyglet (OpenGL components)
* python-rtmidi (MIDI module)
* pyserial (DMX module)
