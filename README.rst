
.. image:: https://bitbucket.org/repo/nnn7Mr/images/2544725897-grail-kit.png
   :height: 200px
   :width: 200px
   :scale: 100%
   :alt: grailkit

Grail Kit
=========

Grailkit is a library for creative and experimental coding. This library used for development of Grail application (http://grailapp.com).
Grailkit includes handling of Project, CueList's, Cue and reading/writing to *.grail files.
Reading and writing to grail bible format.
Also grailkit implements new PyQt5 widgets and dialogs.

Modules and features:

* db - sqlite database wrapper
* osc - Open Sound Control in pure python
* dna - grail format I/O
* dmx - DMX I/O based on RS245
* core - Signals and basic types
* midi - live MIDI input/output
* artnet - Art-Net implementation
* plug - plugin loading/registration
* util - utility functions, constants and classes
* bible - grail bible format I/O
* bible_parse - parsing bible formats to grail format
* graphics - OpenGL graphics context and basic data types like Point, Rectangle, Color

Requirements
------------

This library is Pure Python and depends on following other projects:

* PyQt5 (Qt components in qt module)
* pyglet (OpenGL, app module)
* python-rtmidi (MIDI module)
* pyserial (DMX module)
* pyperclip (clipboard module)
