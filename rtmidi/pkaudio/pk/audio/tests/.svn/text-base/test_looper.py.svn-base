import unittest

from pk.audio import clock
from pk.audio import plugins
from pk.audio import looper
from pk.audio import media
from pk.audio import buffering


class LooperTest(unittest.TestCase):

    def setUp(self):
        self.sound = buffering.Sound(100)
        self.clock = clock.Clock()
        self.sched = plugins.PluggedScheduler(self.sound, self.clock)
        self.looper = looper.Looper()
        self.sched.addPlugin(self.looper)

    def test_loop(self):
        buffering.Filler(media.RandomGenerator(100), self.sound).run()

        stream_out = []
        chunk = buffering.Sound(75)
        self.looper.frames = 50
        self.sched.play(10)
        self.looper.start(10)
        for i in range(10):
            self.clock.set(i*75, 75)
            self.sched.render(chunk)
            stream_out.extend(chunk)
        stream_out = buffering.Sound(seq=stream_out)
            
        predicted = buffering.Sound(len(stream_out))
        frames = []
        i = 10
        while i < len(predicted):
            frames.append(i)
            i += 50
        for frame in frames:
            
            items = len(self.sound)
            if items > len(predicted) - frame:
                items = len(predicted) - frame
                
            dest = predicted[frame:frame+items]
            dest += self.sound[:items]

        self.assertEqual(predicted, stream_out)


if __name__ == '__main__':
    unittest.main()

