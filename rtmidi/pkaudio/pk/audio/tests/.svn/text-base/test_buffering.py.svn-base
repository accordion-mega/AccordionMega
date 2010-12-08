import os
import unittest
import random
from pk.audio import buffering


METRONOME = os.path.join(os.environ['HOME'], '.pksampler/click.wav')

class FillerTest(unittest.TestCase):

    def test_run(self):
        from pk.audio import media
        infile = media.open_wav(METRONOME)
        sound = buffering.Sound(infile.length)
        filler = buffering.Filler(infile, sound)
        filler.run()

    def _test_load(self):
        """ test samplerate conversion. """
        pass

if __name__ == '__main__':
    unittest.main()
