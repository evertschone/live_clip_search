Live Clip Search
================

Info
----

This project contains a Max for Live project and a Python project.  Both
supply different ways of searching for and triggering clips in Ableton
Live.  The Python project works via the LiveOSC UDP server and does not
require Max for Live.

Requirements
------------

To use the Python project you'll need to have LiveOSC installed as a MIDI 
remote script and enabled as a control surface in Live.  You can get LiveOSC 
here:

http://monome.q3f.org/wiki/LiveOSC

You'll also need to have the LiveOSC directory somewhere on your PYTHONPATH.

Usage
---------------------

The Python project has a simple Tk GUI front end and should be relatively
straightforward to use.  Type in a search pattern to return a list of result
clips.  Double click a clip to trigger it in Live.