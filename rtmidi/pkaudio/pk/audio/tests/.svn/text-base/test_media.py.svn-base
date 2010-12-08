"""
Ensure that media wrappers translate media extension behavior properly.
"""

import os
import unittest
from pk.audio import media


class MediaTest:
    
    def test_read_all(self):
        infile = self.Infile(self.fpath)
        length = infile.length
        
        chunk = infile.read(length)
        self.assertEqual(len(chunk), length)

        chunk = infile.read(length)
        self.assertEqual(len(chunk), 0)


def create(superclass, filepath):
    class TestCase(unittest.TestCase, MediaTest):
        Infile = superclass
        fpath = filepath
    return TestCase


WAV = os.path.join(os.environ['HOME'], '.pksampler/click.wav')
SndFileTest = create(media.SndFile, WAV)

OGG = os.path.join(os.environ['HOME'], '.pksampler/click.ogg')
OggTest = create(media.OggFile, OGG)


if __name__ == '__main__':
    unittest.main()
