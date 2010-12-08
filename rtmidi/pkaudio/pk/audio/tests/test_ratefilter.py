import unittest
from pk.audio import media, ratefilter


class RateFilterTest(unittest.TestCase):

    def setUp(self):
        self.media = media.RandomGenerator(10000)
        self.filter = ratefilter.RateFilter()
        self.filter.in_hz = self.media.samplerate

    def _read_all(self):
        stream_out = []
        stream_in = []
        while True:
            chunk = self.media.read(100)
            stream_in.extend(chunk)
            self.filter.write(chunk)
            if self.filter.readable():
                buf = self.filter.read(self.filter.readable())
                stream_out.extend(buf)
            else:
                break
        return stream_in, stream_out

    def test_read_up(self):
        self.filter.out_hz = self.media.samplerate * 2
        stream_in, stream_out = self._read_all()
        self.assertEqual(len(stream_out) > self.media.length, True)

    def test_read_down(self):
        self.filter.out_hz = self.media.samplerate / 2
        stream_in, stream_out = self._read_all()
        self.assertEqual(len(stream_out), self.media.length / 2)

    def test_read_equal(self):
        self.filter.out_hz = self.filter.in_hz
        stream_in, stream_out = self._read_all()
        self.assertEqual(len(stream_out), 10000)


if __name__ == '__main__':
    unittest.main()
    
