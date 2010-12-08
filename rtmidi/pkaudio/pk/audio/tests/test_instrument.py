import unittest
import os.path
from pk.audio import instrument
from pk.audio import flow


METRONOME = os.path.join(os.environ['HOME'], '.pksampler/click.wav')


class InstrumentTest(unittest.TestCase):
    
    def setUp(self):
        self.clock = flow.MusicClock()
        self.instrument = instrument.Instrument(self.clock)

    def test_load(self):
        self.instrument.load(METRONOME)


if __name__ == '__main__':
    unittest.main()

    
