
import os, sys
BUILD_PATHS = [os.path.join(os.getcwd(), 'build/lib.linux-x86_64-2.4/'),
               os.path.join(os.getcwd(), 'build/lib.darwin-8.5.0-Power_Macintosh-2.3/'),
               os.path.join(os.getcwd(), 'build/lib.linux-i686-2.4'),
               ]
sys.path = BUILD_PATHS + sys.path

import sndfile
import numarray
import unittest


class TestSndFile(unittest.TestCase):

    def setUp(self):
        self.sndfile = sndfile.SndFile()
        self.open = lambda: self.sndfile.open('tests/click.wav')
        
    def test_open(self):
        self.open()
        self.assertRaises(sndfile.error, self.open)

        info = self.sndfile.info()
        self.assertEqual(info['format'], 65538)
        self.assertEqual(info['channels'], 2);
        self.assertEqual(info['seekable'], 1);
        self.assertEqual(info['frames'], 4896)
        self.assertEqual(info['samplerate'], 44100);
        self.assertEqual(info['sections'], 1);

        self.sndfile.close()

    def test_read(self):
        self.open()

        for i in (numarray.Bool,
                  numarray.Int8,
                  numarray.UInt8,
                  numarray.Int64,
                  numarray.UInt64,
                  numarray.Complex32,
                  numarray.Complex64):
            fail = lambda: self.sndfile.read(numarray.array([0],  type=i))
            self.assertRaises(sndfile.error, fail)

        chunk = numarray.array([0]*32, type=numarray.Float32)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, len(chunk))

        chunk = numarray.array([0]*32, type=numarray.Int16)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, len(chunk))

        items = 1
        while items:
            chunk *= 0
            items = self.sndfile.read(chunk)
        
        self.sndfile.close()

    def test_overrun_items(self):
        self.open()
        info = self.sndfile.info()
        chunk = numarray.array([0] * info['frames']*2, numarray.Int16)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, len(chunk))

        chunk = numarray.array([0] * info['frames']*2, numarray.Int16)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, 0)

    def test_overrun_frames(self):
        self.open()
        info = self.sndfile.info()
        channels = info['channels']
        chunk = numarray.array([0] * info['frames'] * channels, numarray.Int16)
        
        items = self.sndfile.readf(chunk)
        self.assertEqual(items, len(chunk) / channels)
        self.assertEqual(numarray.any(chunk), True)

        chunk *= 0
        items = self.sndfile.readf(chunk)
        self.assertEqual(items, 0)
        self.assertEqual(numarray.any(chunk), False)

    def test_seek(self):
        self.open()
        info = self.sndfile.info()
        chunk = numarray.array([0] * info['frames'], numarray.Int16)
        
        self.assertEqual(info['seekable'], True)

        off = self.sndfile.seek(info['frames'], sndfile.SEEK_SET)
        #self.assertEqual(off, info['frames']) whaaaat?
        items = self.sndfile.read(chunk)
        self.assertEqual(items, 0)        

        off = self.sndfile.seek(info['frames'] * -1, sndfile.SEEK_CUR)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, info['frames'])

        off = self.sndfile.seek(info['frames'] * -1, sndfile.SEEK_END)
        items = self.sndfile.read(chunk)
        self.assertEqual(items, info['frames'])


if __name__ == '__main__':
    unittest.main()

