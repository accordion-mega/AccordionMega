"""
What?? a numarray ringbuffer?
"""

import numarray


class Empty(Exception):
    pass


class Full(Exception):
    pass


class RingBuffer:
    """ A Sound buffer of static length. """
    def __init__(self, frames=16384):
        self.size = frames
        self.buffer = numarray.array([0] * frames, type=numarray.Float32)
        self._write_cur = 0
        self._read_cur = 0
        self._readable = 0
        
    def readable(self):
        return self._readable

    def writable(self):
        return self.size - self.readable()

    def write(self, chunk):
        items = len(chunk)
        if items <= self.size - self._readable:
            left = self.size - self._write_cur
            if left < len(chunk):
                self.buffer[self._write_cur:] = chunk[:left]
                self.buffer[:items - left] = chunk[left:]
                self._write_cur = items - left
            else:
                self.buffer[self._write_cur:self._write_cur+items] = chunk
                self._write_cur += items
            self._readable += items
        else:
            raise Full('no more room in ringbuffer')

    def read(self, items):
        if items <= self._readable:
            left = self.size - self._read_cur
            if left < items:
                first = numarray.array(self.buffer[self._read_cur:self._read_cur+left])
                second = self.buffer[:items - left]
                chunk = numarray.concatenate((first, second))                
                self._read_cur = items - left
            else:
                chunk = self.buffer[self._read_cur:self._read_cur+items]
                self._read_cur += items
            self._readable -= items
            return chunk
        else:
            raise Empty('not enough items in ringbuffer')

    def reset(self):
        """ untested """
        self._read_cur = 0
        self._write_cur = 0
        self._readable = 0

