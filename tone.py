#!/usr/bin/python3
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk
class Tone(object):

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Tone-Player")
        window.set_default_size(500, 200)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        self.tone_spin = Gtk.SpinButton()
        self.tone_spin.set_range(20, 20000)
        self.tone_spin.set_increments(10, 100)
        self.tone_spin.set_value(300)
        vbox.pack_start(self.tone_spin, False, False, 0)
        self.button = Gtk.Button("Start")
        vbox.add(self.button)
        self.button.connect("clicked", self.start_stop)
        self.tone_spin.connect("value-changed", self.value_change)
        window.show_all()

        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("audiotestsrc", "tone-source")
        audioconv = Gst.ElementFactory.make("audioconvert", "converter")
        audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")
        self.player.add(source)
        self.player.add(audioconv)
        self.player.add(audiosink)
        source.link(audioconv)
        audioconv.link(audiosink)
    def value_change(self, *w):
        tone = float(self.tone_spin.get_value_as_int())
        self.player.get_by_name("tone-source").set_property("freq", tone)

    def start_stop(self, *w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            tone = float(self.tone_spin.get_value_as_int())
            self.player.get_by_name("tone-source").set_property("freq", tone)
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")

GObject.threads_init()
Gst.init(None)
Tone()
Gtk.main()
