"""
peak, rms, decay: things for flashy meters.
"""

import audioop
import numarray


AMP = 20


def float32_to_short16(chunk):
    if chunk.type() != numarray.Float32:
        raise TypeError('chunk must be float32')
    chunk = chunk.copy()
    chunk *= 32768.0
    return chunk.astype(numarray.Int16)


def compute(chunk):
    """ Compute levels for a stereo sound """
    if chunk.type() == numarray.Float32:
        chunk = float32_to_short16(chunk)
    elif chunk.type() != numarray.Int16:
        raise TypeError('sounds must be Int16 or Float32, not',chunk.type())

    def calc_rms(buf):
        return audioop.rms(buf, 2) / 32768.0
    def calc_peak(buf):
        return audioop.avgpp(buf, 2) / 32768.0
    
    sleft = chunk[0::2].tostring()
    sright = chunk[1::2].tostring()
    
    rms = [calc_rms(sleft) * AMP,
           calc_rms(sright) * AMP]
    peak = [calc_peak(sleft) * AMP,
            calc_peak(sright) * AMP]
    decay = [0.0, 0.0]
    return (rms, peak, decay)


class LevelBus:
    """ Calculates rms, peak, and decay values from chunks of
    sound. The values are normalized (0.0 <= x <= 1.0) and stored as
    lists with one element per channel. Considering all audio is
    stereo at the moment, all lists will have two elements.
    """

    rms = None
    peak = None
    decay = None

    def __init__(self):
        self.rms = [0.0, 0.0]
        self.peak = [0.0, 0.0]
        self.decay = [0.0, 0.0]

    def set(self, chunk):
        """ This is the main function, call this from any thread.
        0.0 <= rms, peak, decay <= 1.0
        """
        rms, peak, decay = compute(chunk)
        self.rms = rms
        self.peak = peak
        self.decay = decay
