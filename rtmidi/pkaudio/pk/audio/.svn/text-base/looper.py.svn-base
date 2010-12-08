"""
Helps a scheduler to re-schedule itself 
"""

import plugins


class Looper(plugins.Plugin):

    frames = 44100
    tempo = 140
    
    def __init__(self):
        self._last_frame = None

    def start(self, frame):
        """ a note was kicked off, loop after frame. """
        self._last_frame = frame

    def stop(self):
        """ """
        self._last_frame = None

    def tick(self, sched):
        """ add some events every now and again. """
        if self._last_frame is None:
            return
        next_frame = self._last_frame + self.frames
        if sched.clock.is_now(next_frame):
            sched.add(next_frame)
            self._last_frame = next_frame
