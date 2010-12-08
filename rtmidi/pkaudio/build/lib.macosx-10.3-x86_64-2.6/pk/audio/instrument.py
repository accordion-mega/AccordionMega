"""
pk.audio.scheduler.Scheduler in a flow.Module
"""

import buffering
import plugins
import media
import looper
import flow


CACHESIZE = 20
_cache = []


def find_sound(fpath, samplerate=None):
    global _cache
    for fp, sound in _cache:
        if fp == fpath:
            return sound


    infile = media.open_wav(fpath)
    if not infile is None:
        print 'OPEN %s' % fpath
        sound = buffering.load(infile, samplerate)
        sound *= .1
        if len(_cache) == CACHESIZE:
            _cache = _cache[1:]
        _cache.append((fpath, sound))
        return sound


class BeatLooper(looper.Looper):
    """ beat-wise interface to a frame looper. """

    beats = 1

    def tick(self, sched):
        self.frames = sched.clock.frames_per_beat() * self.beats
        looper.Looper.tick(self, sched)


class Instrument(flow.Module):
    """ It lives again... """

    playing = False
    sched = None
    sound = None
    
    def __init__(self, musicclock):
        flow.Module.__init__(self)
        self.looper = None
        self.clock = musicclock
        self.looping = False
        self.looper = BeatLooper()
        self._soundtempo = None

    def load(self, fpath, tempo=None):
        self.stop()
        self._soundtempo = tempo
        if fpath:
            self.sound = find_sound(fpath, self.clock.samplerate)
            if self.sound is None:
                self.sched = None
                return
            self.sched = plugins.PluggedScheduler(self.sound, self.clock)
            self.sched.addPlugin(self.looper)
            self.checkTempo()
        else:
            self.sound = None
            self.sched = None

    def setLoopBeats(self, beats):
        if self.looper:
            self.looper.beats = int(beats)

    def tick(self, sound):
        if self.sched:
            self.sched.render(sound)

    def play(self, start=None, stop=None):
        if self.sched:
            if start is None:
                start = self.clock.next_beat_frame()
            self.sched.add(start, stop)
            if stop is None and self.looping:
                self.looper.start(start)
            self.playing = True

    def stop(self):
        if self.sched:
            self.sched.clear()
            self.looper.stop()
        self.playing = False

    def loop(self, on):
        self.looping = bool(on)
        if self.looping is False:
            self.looper.stop()

    def checkTempo(self):
        if self.sched and not self._soundtempo is None:
            self.sched.pitch = self.clock.tempo / self._soundtempo

