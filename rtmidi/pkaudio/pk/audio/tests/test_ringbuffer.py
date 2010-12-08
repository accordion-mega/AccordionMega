import unittest
import random
import numarray
from pk.audio import ringbuffer


RINGBUFFER_SIZE = 16384

random.seed()
DATA = []
total = 0
while total < RINGBUFFER_SIZE:
    length = random.randint(1, 1024)
    chunk = []
    for j in range(length):
        chunk.append(random.randint(-32768, 32768))
    DATA.append(numarray.array(chunk, numarray.Int16))
    total += length


class TestRingBuffer(unittest.TestCase):

    def setUp(self):
        self.ringbuffer = ringbuffer.RingBuffer(RINGBUFFER_SIZE)

    def test_01_init(self):
        self.assertEqual(self.ringbuffer.readable(), 0)
        self.assertEqual(self.ringbuffer.writable(), self.ringbuffer.size)
        self.assertRaises(ringbuffer.Empty, lambda: self.ringbuffer.read(1))

    def test_03_reset(self):
        self.ringbuffer.write([0] * 100)
        self.assertEqual(self.ringbuffer.readable(), 100)
        self.assertEqual(self.ringbuffer.writable(), RINGBUFFER_SIZE - 100)
        
        self.ringbuffer.reset()
        self.assertEqual(self.ringbuffer.readable(), 0)
        self.assertEqual(self.ringbuffer.writable(), RINGBUFFER_SIZE)

    def test_04_write(self):
        self.ringbuffer.write(DATA[0])
        self.assertEqual(self.ringbuffer.readable(), len(DATA[0]))
        self.assertEqual(self.ringbuffer.writable(),
                         self.ringbuffer.size - len(DATA[0]))

        self.ringbuffer.write(DATA[1])
        length_in = len(DATA[0]) + len(DATA[1])
        self.assertEqual(self.ringbuffer.readable(), length_in)
        self.assertEqual(self.ringbuffer.writable(),
                         self.ringbuffer.size - length_in)

    def test_05_read(self):
        """ read more than once. """
        first = 500
        second = 501
        stream_in = [1] * (first + second)
        self.ringbuffer.write(stream_in)
        self.assertEqual(self.ringbuffer.readable(), len(stream_in))

        chunk = self.ringbuffer.read(first)
        self.assertEqual(self.ringbuffer.readable(), second)
        self.assertEqual(len(chunk), len(stream_in[:first])) # no nasty output

        chunk = self.ringbuffer.read(second)
        self.assertEqual(len(chunk), second) # no nasty output


    def test_06_equal_pointer(self):
        self.ringbuffer.write([1,2,3])
        self.ringbuffer.read(3)
        self.assertEqual(self.ringbuffer._write_cur,
                         self.ringbuffer._read_cur)

        in_2 = [4] * self.ringbuffer.size
        self.ringbuffer.write(in_2)
        self.assertEqual(self.ringbuffer._write_cur,
                         self.ringbuffer._read_cur)

        ret = self.ringbuffer.read(self.ringbuffer.size)
        self.assertEqual(self.ringbuffer._read_cur, 3)

    def test_07_write_read_wrap(self):
        stream_in = []
        i = 0
        while len(DATA[i]) < self.ringbuffer.writable():
            stream_in.extend(DATA[i])
            self.ringbuffer.write(DATA[i])
            i += 1
        self.assertRaises(ringbuffer.Full,
                          lambda: self.ringbuffer.write(DATA[i]))

        stream_out = self.ringbuffer.read(len(stream_in))
        self.assertEqual(self.ringbuffer.readable(), 0)
        self.assertEqual(self.ringbuffer.writable(), self.ringbuffer.size)
        self.assertEqual(list(stream_in), list(stream_out))

        stream_in = DATA[i]
        self.ringbuffer.write(stream_in) # should wrap
        self.assertEqual(self.ringbuffer.readable(), len(stream_in))
        self.assertEqual(self.ringbuffer.writable(),
                         self.ringbuffer.size - len(stream_in))

        stream_out = self.ringbuffer.read(len(stream_in))
        self.assertEqual(self.ringbuffer.readable(), 0)
        self.assertEqual(self.ringbuffer.writable(), self.ringbuffer.size)

        # this test does not test for
        # first = numarray.array(self.buffer[self._read_cur:left])
        # in read


if __name__ == '__main__':
    unittest.main()
