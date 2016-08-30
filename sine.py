#!/usr/bin/python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import math, time

f = lambda t: math.sin(t) * 450 + 550

Gst.init(None)
player = Gst.Pipeline.new("player")
source = Gst.ElementFactory.make("audiotestsrc", "tone-source")
audioconv = Gst.ElementFactory.make("audioconvert", "converter")
audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")
player.add(source)
player.add(audioconv)
player.add(audiosink)
source.link(audioconv)
audioconv.link(audiosink)

player.set_state(Gst.State.PLAYING)
source.set_property("wave", 1)
for i in range(500):
    source.set_property("freq", f(i/100 * math.pi))
    time.sleep(0.02)
    i += 1
player.set_state(Gst.State.NULL)

