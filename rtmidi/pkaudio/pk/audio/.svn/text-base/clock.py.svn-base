"""
frame-time computations
"""

def within(x, y, z):
    return z >= x and z < y


class Clock:
    """ Calculates period-wise values. """

    periodstart = 0
    periodstop = 0
    periodsize = 0
    samplerate = 44100

    def set(self, periodstart, periodsize):
        self.periodstart = periodstart
        self.periodstop = self.periodsize - periodstart
        self.periodsize = periodsize

    def is_now(self, frame):
        x = self.periodstart
        y = self.periodstart + self.periodsize
        z = frame
        return z >= x and z < y

    def is_past(self, frame):
        return frame < self.periodstart
