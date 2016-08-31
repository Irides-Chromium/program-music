#!/usr/bin/python3
# URL: https://musescore.com/user/204596/scores/204751
import os
from time import sleep
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
piano = lambda a: 2 ** ((a - 49) / 12) * 440
octave = 4
timing = 0.25
keys = {'c': 1, 'd': 3, 'e': 5, 'f': 6, 'g': 8, 'a': 10, 'b': 12,
        'c#': 2, 'd#': 4, 'f#': 7, 'g#': 9, 'a#': 11}
name = ['00', 'c ', 'c#', 'd ', 'd#', 'e ', 'f ', 'f#', 'g ', 'g#', 'a ', 'a#', 'b ']
tracks = [[] for i in range(8)]
tracks = [
        [(68, 1), (68, 1), (0, 1), (68, 1), (0, 1), (63, 1), (68, 2), (61, 2), (0, 2), (0, 2), (0, 2)],
        [(58, 1), (57, 1), (0, 1), (57, 1), (0, 1), (57, 1), (57, 2), (59, 2), (0, 2), (59, 2), (0, 2)],
        [(42, 1), (42, 1), (0, 1), (42, 1), (0, 1), (42, 1), (42, 2), (47, 2), (0, 2), (47, 2), (0, 2)],
        [],[],[],[],[]]
track_ptr = 0
#tracks[0] = [(44, 1), (44, 1), (45, 1), (47, 1), (47, 1), (45, 1), (44, 1), (42, 1), (40, 1), (40, 1), (42, 1), (44, 1), (44, 2), (42, 0.5), (42, 0.5), (0, 1), (44, 1), (44, 1), (45, 1), (47, 1), (47, 1), (45, 1), (44, 1), (42, 1), (40, 1), (40, 1), (42, 1), (44, 1), (42, 2), (40, 0.5), (40, 0.5)]

class event:
    """A single playable event with a key (note) and tick (time)"""
    def __init__(self, key, tick):
        self.key = key
        self.tick = tick

    def __str__(self):
        return "({}: {:.2f})".format(self.name[key - 1], self.tick)

    @staticmethod
    def start_playback(player):
        player.set_state(Gst.State.PLAYING)

    def play_con(source):
        if self.key:
            source.set_property("freq", piano(octave[self.key - 1]))
            sleep(tick * 0.5 - 0.07)

    def silence(source): 
        source.set_property("wave", 4) # Silence
        sleep(tick * 0.5)
        source.set_property("wave", 0)

    @staticmethod
    def stop_playback(player):
        player.set_state(Gst.State.NULL)

def add_event(key, tick):
    tick = int(tick)
    if key == '0': tracks[track_ptr].append((0, tick))
    else: tracks[track_ptr].append(( \
            keys[key.lower()] + (octave - 1) * 12 + 3, tick))

def add_events(events):
    if len(events) % 2 != 0: raise ValueError("Error in events.")
    for i in range(len(events))[::2]:
        add_event(*events[i:i + 2])

# use beep
# os.system("sudo modprobe pcspkr")
# def play_track(track):
#     for key, tick in track:
#         if key: os.system("beep -f {freq} -l {length}" \
#                 .format(freq=piano(octave[key-1]), length=tick * 500))
#         else: os.system("sleep {length}".format(length=tick * 0.5))

# Use Gst
def play_track(track):
    Gst.init()
    player = Gst.Pipeline.new("player")
    source = Gst.ElementFactory.make("audiotestsrc", "tone-source")
    audioconv = Gst.ElementFactory.make("audioconvert", "converter")
    audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")
    player.add(source)
    player.add(audioconv)
    player.add(audiosink)
    source.link(audioconv)
    audioconv.link(audiosink)
    source.set_property("wave", 3)
    player.set_state(Gst.State.PLAYING)

    for key, tick in track:
        if key:
            source.set_property("freq", piano(key))
            sleep(tick * timing * 0.25)
            source.set_property("freq", 0) # Silence
            sleep(tick * timing * 0.75)
        else:
            source.set_property("wave", 4) # Silence
            sleep(tick * timing)
            source.set_property("wave", 3)
    player.set_state(Gst.State.NULL)

def play_tracks(tracks):
    from multiprocessing import Pool
    p = Pool(8)
    p.map(play_track, tracks)

def print_track(track):
    count = 0
    if len(track) == 0: print("Nothing in track.")
    else:
        for key, tick in track:
            if count % 10 == 0: print()
            print(name[(key - 3) % 12 if key else 0] + ": {:.1f} ".format(tick), end="")
            count += 1
        print()

def print_tracks(tracks):
    for i in range(8):
        print("Track {}:".format(i))
        print_track(tracks[i])

if __name__ == '__main__':
    while True:
        try: cmd = input(">>> ")
        except (KeyboardInterrupt, EOFError): exit()
        command = cmd.split()
        if len(command) == 0: continue
        action, *args = command
        action = action.lower()
        if action == 'add': add_event(*args)
        elif action == 'clear': tracks = [[] for i in range(8)]
        elif action == 'play': play_tracks(tracks)
        elif action == 'quit': exit()
        elif action == 'disp': print_tracks(tracks)
        elif action == 'set':
            if len(args) == 1:
                if args[0] == "tick": print(timing)
                elif args[0] == "octave": print(octave)
                elif args[0] == "track": print(track_ptr)
            elif len(args) > 1:
                if args[0] == "tick": timing = float(args[1])
                elif args[0] == "octave": octave = int(args[1])
                elif args[0] == "track": track_ptr = \
                    {'high': 0, 'low': 4}[args[1]] + int(args[2]) - 1
        elif action == 'raw':
            for track in tracks: print(track)
