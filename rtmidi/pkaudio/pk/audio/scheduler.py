""" Timing functions (write this there)

 * Events are stored but not efficient, so don't store a whole song on
   the scheduler.

 * Ratefilter muddles the writer's stop frame, so clock jumps make
   correcting playing events and cleaning stale events a pain. Save
   this for the future.
 
"""

RESAMPLE = False


class Writer:
    """ performs a scheduled event. """
    
    pos = 0
    done = False
    chunksize = 10

    def __init__(self, sound):
        self.sound = sound

    def setpitch(self, pitch):
        pass

    def reset(self):
        """ re-use before re-cycle! """
        self.pos = 0
        self.done = False

    def write(self, target):
        """ render according to internal attributes. """
        items = len(self.sound) - self.pos
        if items > len(target):
            items = len(target)
        chunk = self.sound[self.pos:self.pos+items]
        target[:items] += chunk
        self.pos += items
        if self.pos == len(self.sound):
            self.done = True


class Scheduler:
    """ Polyphonic scheduler
    Starts a writer on each frame requested.
    """

    pitch = 1.0

    def __init__(self, sound, clock):
        self.sound = sound
        self.clock = clock
        self.cache = []
        self.rolling = []
        self.pending = []

    def add(self, start, stop=None):
        """ Play a note on a frame - dictate polyphonic policy
        """
        if start < self.clock.periodstart:
            return # stale
        if self.cache:
            writer = self.cache.pop(-1)
        elif not self.cache:
            writer = Writer(self.sound)
        self.pending.append((start, writer))
        #print 'ADDING event @ %s' % start

    def clear(self):
        self.cache = []
        self.rolling = []
        self.pending = []

    def render(self, target):
        """ called every interrupt """
        pending = list(self.pending)
        rolling = list(self.rolling)

        for frame, writer in pending:
            if self.clock.is_now(frame):
                offset = frame - self.clock.periodstart
                writer.reset()
                writer.setpitch(self.pitch)
                writer.write(target[offset:])
                self.rolling.append(writer)
                self.pending.remove((frame, writer))
            elif self.clock.is_past(frame):
                self.pending.remove((frame, writer))

        for writer in rolling:
            writer.setpitch(self.pitch)
            writer.write(target)
            if writer.done:
                self.rolling.remove(writer)
                self.cache.append(writer)



