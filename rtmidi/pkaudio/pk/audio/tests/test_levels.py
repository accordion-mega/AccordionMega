import unittest
import numarray
from pk.audio import levels


class LevelsTest(unittest.TestCase):
    
    def test_compute(self):
        from pk.audio import instrument
        chunk = instrument.find_sound('/Users/patrick/.pksampler/click.wav')
        #chunk = numarray.array([0] * 1000, type=numarray.Float32)
        rms, peak, decay = levels.compute(chunk)
        self.assertEqual(len(rms), 2)
        self.assertEqual(len(peak), 2)
        self.assertEqual(len(decay), 2)        
        for i in range(2):
            self.assertEqual(rms[i] <= 1.0 and rms[i] >= 0.0, True)
            self.assertEqual(peak[i] <= 1.0 and peak[i] >= 0.0, True)
            self.assertEqual(decay[i] <= 1.0 and decay[i] >= 0.0, True)


if __name__ == '__main__':
    unittest.main()
    
