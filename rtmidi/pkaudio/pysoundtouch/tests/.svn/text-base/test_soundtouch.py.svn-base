import os, sys
BUILD_PATHS = [os.path.join(os.getcwd(), 'build/lib.linux-x86_64-2.4/'),
               os.path.join(os.getcwd(), 'build/lib.darwin-8.5.0-Power_Macintosh-2.3/'),
               ]
sys.path = BUILD_PATHS + sys.path

import soundtouch
import unittest
import numarray
from pk.audio import buffering
from pk.audio import media


class SoundTouchTest(unittest.TestCase):

    def setUp(self):
        self.st = soundtouch.SoundTouch()

    def _test_find_bpm(self):
        infile = media.SndFile('tests/drums.wav')
        sound = buffering.Sound(length=infile.length)
        buffering.Filler(infile, sound).run()
        tempo = soundtouch.find_bpm(sound, sound.samplerate)
        self.assertEqual(type(tempo), float)
        self.assertEqual(int(tempo), 64)

    def test_init(self):
        self.st.setSampleRate(44100)
        self.assertEqual(self.st.isEmpty(), True)
        self.assertEqual(self.st.numSamples(), 0)
        
        self.st.setRate(44444)
        #self.assertEqual(self.st.rate, 44444)

        self.st.setTempo(149.1)
        #self.assertEqual(int(self.st.tempo), 149)

        self.assertRaises(RuntimeError, lambda: self.st.setChannels(3))

        self.st.setChannels(2)
        #self.assertEqual(self.st.channels, 3)

    def test_filter(self):
        self.st.setSampleRate(44100)
        self.st.setChannels(2)
        self.st.setRate(1.0)
        self.st.setRateChange(50)
        
        stream_in = numarray.array([1] * 100)
        self.st.putSamples(stream_in)
        samples = self.st.numSamples()
        self.assertEqual(samples > 0, True)
        self.assertEqual(self.st.isEmpty(), False)

        stream_out = numarray.array([0] * 110);
        returned = self.st.receiveSamples(stream_out)
        self.assertEqual(returned, samples)
        self.assertEqual(self.st.isEmpty(), True)


if __name__ == '__main__':
    unittest.main()
