
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
* artnet - Artistic License Art-Net (tm) implementation (experimental)

GUI:

* qt - Qt components
* app - pyglet application classes (experimental)
* graphics - OpenGL graphics context and basic data types like Point, Rectangle, Color (experimental)
* clipboard - access OS clipboard (experimental)


Requirements
------------

This library is Pure Python and depends on following other projects:

* PyQt5 (Qt components in qt module)
* pyglet (OpenGL, app module)
* python-rtmidi (MIDI module)
* pyserial (DMX module)
* pyperclip (clipboard module)
