"""
high-level audio/music components.

channel => module => [ module -> sched ]

sound = Instrument()
sound.load(WAV)
sound.loop(True)
volume = Volume()
channel = Channel([sound, volume])

mixer = Mixer()
mixer.attach(channel)
mixer.start()
"""

import time
import media
import clock
import output
import buffering
import levels


LEVELS = True


class Module:
    """ A part of a channel. """
    def __init__(self):
        self.levelbus = levels.LevelBus()

    def render(self, sound):
        self.tick(sound)
        if LEVELS:
            self.levelbus.set(sound)
        
    def tick(self, sound):
        """ another name? """
        pass

    def setTempo(self, tempo):
        pass


class Channel(list):
    """ Module container.
    This could (should?) become a graph later.
    """

    sound = None

    def periodsize(self, frames):
        if not self.sound is None and len(self.sound) != frames:
            print 'resizing %i => %i' % (len(self.sound), frames)
        self.sound = buffering.Sound(frames)

    def execute(self):
        self.sound *= 0
        for module in self:
            module.render(self.sound)
        return self.sound


class MusicClock(clock.Clock):
    """ Global audio settings, music computations. """
    
    last_beat_frame = 0 # fix this concept
    tempo = 140.0

    def frames_per_beat(self):
        channels = 2
        bps = float(self.tempo) / 60 / channels
        return int(self.samplerate / bps) / 2

    def set(self, start, length):
        # pay respect to clock skew
        fpb = self.frames_per_beat()
        while self.is_past(self.last_beat_frame + fpb):
            self.last_beat_frame += fpb
        clock.Clock.set(self, start, length)

    def next_beat_frame(self):
        return self.last_beat_frame + self.frames_per_beat()

    def set_tempo(self, tempo):
        self.tempo = tempo
        for channel in list(self.channels):
            for module in channel:
                module.setTempo(self.tempo)

    def change_tempo(self, delta):
        self.tempo += delta
        self.set_tempo(self.tempo)


class Mixer(output.Output, MusicClock):
    """ Executes the channels, writes to output. """
    def __init__(self):
        output.Output.__init__(self)
        self.levelbus = levels.LevelBus()
        self.channels = []
        self.lasttime = 0

    def set_periodsize(self, value):
        self.periodsize = value
        for i in self.channels:
            i.periodsize(value)

    def attach(self, channel):
        channel.periodsize(self.periodsize)
        self.channels.append(channel)

    def render(self, chunk):
        start = time.time()
        self.set(self.frame_time, len(chunk))
        for channel in list(self.channels):
            temp = channel.execute()
            chunk += temp
        self.lasttime += len(chunk)
        if LEVELS:
            self.levelbus.set(chunk)
        end = time.time()
        #print 'TIME: %0.3f' % (end - start)
        output.Output.render(self, chunk)


## SOME MISC MODULES
## move this somewhere else later


class Volume(Module):

    left = 1.0
    right = 1.0

    def tick(self, sound):
        if self.left == self.right:
            sound *= self.left
        else:
            for i in range(len(sound)):
                if i % 2:
                    sound[i] *= self.right
                else:
                    sound[i] *= self.left


class Merger(Module):

    def __init__(self):
        Module.__init__(self)
        self.modules = []

    def attach(self, module):
        if not module in self.modules:
            self.modules.append(module)

    def detach(self, module):
        if module in self.modules:
            self.modules.remove(module)

    def tick(self, sound):
        for m in list(self.modules):
            m.tick(sound)


class Ladspa(Module):

    name = None

    def __init__(self, name):
        Module.__init__(self)
        name = name

    def tick(self, sound):
        pass
