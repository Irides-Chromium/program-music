#!/usr/bin/python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from time import sleep

Gst.init(None)
piano = lambda a: 2 ** ((a - 49) / 12) * 440

player = [Gst.Pipeline.new("player%d" % i) for i in range(3)]
source = [Gst.ElementFactory.make("audiotestsrc", "tone-source%d" % i) for i in range(3)]
audioconv = [Gst.ElementFactory.make("audioconvert", "converter%d" % i) for i in range(3)]
audiosink = [Gst.ElementFactory.make("autoaudiosink", "audio-output%d" % i) for i in range(3)]

for i in range(3):
    player[i].add(source[i])
    player[i].add(audioconv[i])
    player[i].add(audiosink[i])
    source[i].link(audioconv[i])
    audioconv[i].link(audiosink[i])
source[0].set_property("freq", piano(42))
#source[1].set_property("freq", piano(44))
#source[2].set_property("freq", piano(47))
player[0].set_state(Gst.State.PLAYING)
#player[1].set_state(Gst.State.PLAYING)
#player[2].set_state(Gst.State.PLAYING)
sleep(2)
player[0].set_state(Gst.State.NULL)
player[1].set_state(Gst.State.NULL)
player[2].set_state(Gst.State.NULL)
