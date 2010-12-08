"""
Resample sound.
"""

import audioop
import numarray
import ringbuffer


CHANNELS = 2
BUFFERSIZE = 16384


class RateFilter(ringbuffer.RingBuffer):

    out_hz = 0
    in_hz = 0
    _state = None

    def write(self, in_array):
        """ prepare at least 'items' samples.
        """
        fragment, self.state = audioop.ratecv(in_array,
                                              2,
                                              CHANNELS,
                                              self.in_hz,
                                              self.out_hz,
                                              self._state)
        ar = numarray.fromstring(fragment, type=numarray.Int16)
        ringbuffer.RingBuffer.write(self, ar)

    def reset(self):
        self.state = None
        return ringbuffer.RingBuffer.reset(self)
