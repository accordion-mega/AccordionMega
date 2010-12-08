import unittest
from pk.audio import buffering
from pk.audio import flow


class LambdaModule(flow.Module):

    count = 0

    def __init__(self, func):
        flow.Module.__init__(self)
        self.func = func
        self.stream_out = []

    def tick(self, chunk):
        self.func(chunk)
        self.stream_out.extend(chunk)
        self.count += 1


# TODO: make these order-specific
def fix1(chunk):
    chunk += 1
def fix2(chunk):
    chunk += 2


class TestChannel(flow.Channel):
    def __init__(self, *args):
        self.mod1 = LambdaModule(fix1)
        self.mod2 = LambdaModule(fix2)
        list.__init__(self, [self.mod1, self.mod2])


class ChannelTest(unittest.TestCase):

    def setUp(self):
        self.channel = TestChannel()
        self.mod1 = self.channel[0]
        self.mod2 = self.channel[1]

    def test_periodsize(self):
        self.channel.periodsize(512)
        self.assertEqual(len(self.channel.sound), 512)

    def test_tick(self):
        """ all modules must be ticked. """
        stream_out = []
        self.channel.periodsize(75)
        for i in range(10):
            chunk = self.channel.execute()
            stream_out.extend(chunk)
        stream_out = buffering.Sound(seq=stream_out)

        mod1_out = buffering.Sound(seq=self.mod1.stream_out)
        mod2_out = buffering.Sound(seq=self.mod2.stream_out)

        self.assertEqual(self.mod1.count, 10)
        self.assertEqual(self.mod2.count, 10)
        self.assertEqual(len(stream_out), len(mod1_out))
        self.assertEqual(len(stream_out), len(mod2_out))

        predicted = buffering.Sound(len(stream_out))
        fix1(predicted)
        fix2(predicted)
        self.assertEqual(list(predicted), list(stream_out))


class MixerTest(unittest.TestCase):

    def setUp(self):
        self.channel1 = TestChannel()
        self.channel2 = TestChannel()
        self.mixer = flow.Mixer()
        self.mixer.periodsize = 100
        self.mixer.attach(self.channel1)
        self.mixer.attach(self.channel2)

    def test_attach(self):
        channels = [flow.Channel() for i in range(5)]
        for c in channels:
            self.mixer.attach(c)

        sizes = [len(channel.sound) for channel in channels]
        self.assertEqual(sizes, [self.mixer.periodsize] * len(channels))

    def test_render(self):
        stream_out = []
        chunk = buffering.Sound(100)
        for i in range(5):
            chunk *= 0
            self.mixer.render(chunk)
            stream_out.extend(chunk)

        predicted = buffering.Sound(500)
        fix1(predicted)
        fix2(predicted)
        fix1(predicted)
        fix2(predicted)
        self.assertEqual(list(predicted), stream_out)
        

if __name__ == '__main__':
    unittest.main()
    
        
