"""
Media support.
"""


import random
import math
import numarray
import buffering
import ringbuffer


try:
    import ogg.vorbis
    HAS_OGG = True
except ImportError, e:
    HAS_OGG = False

try:
    import sndfile
    HAS_SNDFILE = True
except ImportError, e:
    HAS_SNDFILE = False

random.seed()


class Media:
    """ A source of raw audio frames. """

    length = 0
    samplerate = 0
    channels = 2 # ?

    def reset(self):
        pass
    
    def read(self, items):
        """ return an array of requested length. Return maximum
        possible if not enough data. 
        """
        raise RuntimeError('%s.read: not implemented!' % self.__class__)
        

class RandomGenerator(Media):
    """ Good for testing. """

    samplerate = 44100
    channels = 2
    
    def __init__(self, length):
        self.length = length
        self.pos = 0

    def fix(self, i):
        return i and i or 1

    def reset(self):
        self.pos = 0
        
    def read(self, items):
        import random
        if self.pos >= self.length:
            return buffering.Sound(0)
        elif self.pos + items > self.length:
            items = self.length - self.pos
        self.pos += items
        items = [self.fix(random.randint(-32768, 32768))
                 for i in range(items)]
        return buffering.Sound(seq=items)


class SineOutput(Media):

    offset = 0
    samplerate = 44100

    def read(self, items):
        chunk = self.render_short(items)
        return numarray.array(chunk, numarray.Int16)

    def float_to_short(self, f):
        return int(f * 32768)

    def render_short(self, items):
        ret = self.render_float(items)
        return [self.float_to_short(f) for f in ret]

    def render_float(self, items):
        offset = self.offset
        ret = [
            0.2 * math.sin(3.1415*440.0/self.samplerate*(frame+offset))
            for frame in range(items)
        ]
        self.offset += items
        return ret


class _SndFile(Media):
    """ libsndfile """
    def __init__(self, fpath):
        import dsptools.sndfile
        self.fpath = fpath
        self.file = dsptools.sndfile.open(fpath)
        self.samplerate = self.file.info.samplerate
        self.length = self.file.info.frames * 2

    def __str__(self):
        return 'SndFile: %s' % self.fpath
        
    def read(self, items):
        ar, items = self.file.read(items)
        return ar[:items]

    def reset(self):
        self.file.reset()
        Source.reset(self)


class SndFile(Media):
    def __init__(self, fpath):
        import sndfile
        self.fpath = fpath
        self.infile = sndfile.SndFile()
        self.infile.open(fpath)
        info = self.infile.info()
        self.samplerate = info['samplerate']
        self.channels = info['channels']
        self.length = info['frames'] * self.channels
        
    def __str__(self):
        return 'SndFile: %s' % self.fpath
        
    def read(self, items):
        chunk = numarray.array([0] * items, type=numarray.Float32)
        items = self.infile.read(chunk)
        return chunk[:items]

    def reset(self):
        self.file.reset()
        Source.reset(self)


import struct
class OggFile(Media):
    """ ogg.vorbis """

    samplerate = 44100

    def __init__(self, fpath):
        self.vf = ogg.vorbis.VorbisFile(fpath)
        info = self.vf.info()
        self.samplerate = info.rate
        self.length = self.vf.pcm_total() * 2
        self.ringbuffer = ringbuffer.RingBuffer()

    def read(self, items):
        while self.ringbuffer.readable() < items:
            buff, bytes, bitstream = self.vf.read(4096)
            if bytes == 0: break
            buff = buff[:bytes] # geeze...
            seq = struct.unpack('H' * (len(buff) / 2), buff)
            chunk = numarray.array(seq, type=numarray.Int16)
            self.ringbuffer.write(chunk)
        if items > self.ringbuffer.readable():
            items = self.ringbuffer.readable()
        return self.ringbuffer.read(items)
            

def extension(fpath):
    """ return the extension of fpath, not including the . """
    return fpath[fpath.rfind('.')+1:]


_TYPES = {}
if HAS_OGG:
    _TYPES[('ogg',)] = OggFile
if HAS_SNDFILE:
    _TYPES[('wav', 'aiff',)] = SndFile


def can_open(fpath):
    try:
        open_wav(fpath)
        return True
    except:
        return False


def supported(fpath):
    ext = extension(fpath).lower()
    for types, ctor in _TYPES.items():
        if ext in types:
            return True
    return False
    

def open_wav(fpath):
    ext = extension(fpath).lower()
    for types, ctor in _TYPES.items():
        if ext in types:
            return ctor(fpath)
    raise KeyError('file not supported')

