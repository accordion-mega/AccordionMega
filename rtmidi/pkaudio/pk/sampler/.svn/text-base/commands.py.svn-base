"""
real-time state scripting

Commands operate on data, but we don't have data we have a
state. There is no undo, just selecting a different state. fun fun!

CONTROLS
    volume
    start/stop
"""


def midi_validate(x):
    if x < 0 or x > 127:
        raise ValueError('invalid midi value (%s)' % value)


class Control:
    """ Stores midi values. """
    def validate(self, value):
        midi_validate(value)
    def set(self, name, value):
        pass
    def get(self, name):
        pass


class State:
    """ Encapsulates a set of commands that you couldn't possibly
    perform all at once.
    """

    controls = None
    patterns = None

    def __init__(self):
        self.controls = {}
        self.values = {}
        self.loops = []

    def set(self):
        for name, value in self.values.items():
            self.controls[name].set(value)
        for loop in self.loops:
            self.sequencer.play(loop)

    def toelem(self, element):
        return
        head = elementtree.SubElement(element, 'state')
        for name, value in self.values.items():
            elem = elementtree.SubElement(element, 'control')
            elem.set('name', name)
            elem.set('value', str(value))
        for loop in self.loop:
            elem = elementtree.SubElement(element, 'loop')
            elem.set('name', name)


class Manager:
    """ set state on sampler """
    
    sampler = None
    
    def set(self, state):
        self.sampler.clear_state()
        state.sampler = self.sampler
        self.state.set()
