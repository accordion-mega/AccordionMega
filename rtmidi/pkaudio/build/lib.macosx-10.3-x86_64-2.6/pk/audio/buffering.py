"""
Functions related to memory storage.
"""

import time
import threading
import numarray
import ratefilter


RESAMPLE = True
TYPE = numarray.Float32


def Sound(items=None, seq=None):
    if not items is None:
        return numarray.array([0] * items, type=TYPE)
    elif not seq is None:
        return numarray.array(seq, type=TYPE)


class Filler:
    """ buffer filler """

    chunksize = 1000
    
    def __init__(self, infile, sound, samplerate=None):
        self.sound = sound
        self.infile = infile
        self.ratefilter = ratefilter.RateFilter()
        #self.ratefilter.in_hz = infile.samplerate
        #self.ratefilter.out_hz = samplerate
        self.samplerate = samplerate
        self._write_cur = 0

    def prep(self, chunk):
        if RESAMPLE and self.ratefilter.in_hz != self.ratefilter.out_hz:
            self.ratefilter.write(ar)
            items = self.ratefilter.readable()
            chunk = self.ratefilter.read(items)
        return chunk

    def write(self, chunk):
        """ return number of items written """
        items = len(chunk)
        if items > len(self.sound) - self._write_cur:
            raise ValueError('not enough room in Sound buffer')
        dest = self.sound[self._write_cur:self._write_cur+items]
        dest += chunk
        self._write_cur += items
        return items

    def run(self):
        """ fill the sound, perform conversions. """
        start = time.time()
        total = 0
        while True:
            chunk = self.infile.read(self.chunksize)
            total += len(chunk)
            if len(chunk):
                self.write(chunk)
            else:
                break
        ms = (time.time() - start) * 1000.0
        msg = 'FILLED %s (%i frames in %f ms)' % (self.infile,
                                                  self.infile.length,
                                                  ms)
        #print msg
        self.full = True


def load(infile, samplerate):
    sound = Sound(infile.length)
    filler = Filler(infile, sound, samplerate)
    filler.run()
    return sound


def startfill(infile, sound):
    """ ensure the lifetime of the thread. """
    filler = Filler(infile, sound)
    thread = threading.Thread(target=filler.run)
    thread.setDaemon(True) # die even if running
    thread.start()
    return thread
