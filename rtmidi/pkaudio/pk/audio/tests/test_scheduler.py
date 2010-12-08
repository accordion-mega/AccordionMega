import unittest
import numarray
import random
from pk.audio import scheduler
from pk.audio import media
from pk.audio import buffering
from pk.audio import clock


random.seed()


class WriterTest(unittest.TestCase):

    def setUp(self):
        self._scheduler_RESAMPLE = scheduler.RESAMPLE
        self.infile = media.RandomGenerator(100)
        self.sound = self.infile.read(100)
        self.writer = scheduler.Writer(self.sound)

    def test_write(self):
        scheduler.RESAMPLE = self._scheduler_RESAMPLE
        stream_out = buffering.Sound(1000)
        self.writer.write(stream_out)
        self.assertEqual(numarray.all(self.sound[:100]), True)
        self.assertEqual(numarray.any(self.sound[100:]), False)

    def test_write_many(self):
        """ test that a writer writes and seeks correctly. """
        stream_out = buffering.Sound(100)
        for i in range(10):
            self.writer.write(stream_out[i*10:i*10+10])
        self.assertEqual(list(self.sound), list(stream_out))

        if scheduler.RESAMPLE is False:
            self.assertEqual(self.writer.done, True)

    def test_mix(self):
        """ test that writers mix audio correctly. """
        stream_out = buffering.Sound(500)
        predicted = buffering.Sound(500)
        predicted[200:300] += self.sound
        predicted[250:350] += self.sound

        writer_one = scheduler.Writer(self.sound)
        writer_two = scheduler.Writer(self.sound)
        writer_one.write(stream_out[200:])
        writer_two.write(stream_out[250:])
        self.assertEqual(list(stream_out), list(predicted))
        self.assertEqual(numarray.any(stream_out[:200]), False)
        self.assertEqual(numarray.any(stream_out[350:]), False)

    def _test_resample(self):
        items = 100
        chunk = buffering.Sound(items)
        self.writer._resample(items)
        self.assertEqual(self.writer.ratefilter.readable() >= items, True)

        readable = self.writer.ratefilter.readable()
        stream_out = self.writer.ratefilter.read(readable)
        self.assertEqual(self.writer.ratefilter.readable(), 0) # what the heck?

    def test_reset(self):
        """ test write() after a reset. """
        chunk = buffering.Sound(100)
        self.writer.write(chunk)
        self.assertEqual(list(chunk), list(self.sound[:len(chunk)]))

        chunk *= 0
        self.writer.reset()
        self.writer.write(chunk)
        self.assertEqual(list(chunk), list(self.sound[:len(chunk)]))

        chunk *= 0
        self.writer.reset()
        self.writer.write(chunk)
        self.assertEqual(list(chunk), list(self.sound[:len(chunk)]))

    def _test_setpitch(self):
        """ whitebox rate test. """
        items = len(self.sound) / 10
        chunk = buffering.Sound(items)

        # set samplerate up
        self.writer.reset()
        self.writer.setpitch(.5)
        self.writer._resample(items)
        self.assertEqual(self.writer.ratefilter.readable() >= items, True)
        
        # set samplerate down
        self.writer.reset()
        self.writer.setpitch(2.0)
        self.writer._resample(items)
        self.assertEqual(self.writer.ratefilter.readable() >= items, True)


    def _test_pitchslide(self):
        # oh man...
        pass
    


class SchedulerTest(unittest.TestCase):

    def setUp(self):
        self._scheduler_RESAMPLE = scheduler.RESAMPLE
        scheduler.RESAMPLE = True
        self.sound = buffering.Sound(100)
        buffering.Filler(media.RandomGenerator(100), self.sound).run()
        self.periodsize = 75
        self.clock = clock.Clock()
        self.sched = scheduler.Scheduler(self.sound, self.clock)
        
    def tearDown(self):
        scheduler.RESAMPLE = self._scheduler_RESAMPLE

    def test_events(self):
        scheduler.RESAMPLE = False
        def pending():
            return [e[0] for e in self.sched.pending]
        chunk = buffering.Sound(75)
        
        self.assertEqual(self.sched.rolling, [])
        
        self.sched.add(100)
        self.sched.add(200)
        self.sched.add(300)
        self.clock.set(20, 75)
        self.sched.render(chunk)
        self.assertEqual(pending(), [100, 200, 300])
        self.assertEqual(len(self.sched.rolling), 0)

        self.clock.set(90, 75)
        self.sched.render(chunk)
        self.assertEqual(pending(), [200, 300])
        self.assertEqual(len(self.sched.rolling), 1)
        
        self.clock.set(200, 75)
        self.sched.render(chunk)
        self.assertEqual(pending(), [300])
        self.assertEqual(len(self.sched.rolling), 1)

        # for overlap
        self.sched.add(390)

        self.clock.set(290, 75)
        self.sched.render(chunk)
        self.assertEqual(pending(), [390])
        self.assertEqual(len(self.sched.rolling), 1)

        self.clock.set(365, 75)
        self.sched.render(chunk)
        self.assertEqual(pending(), [])
        self.assertEqual(len(self.sched.rolling), 1)

    def test_one(self):
        sound_start = 400
        sound_stop = sound_start + len(self.sound)

        self.sched.add(sound_start)
        stream_out = []
        target = numarray.array([0] * self.periodsize, numarray.Int16)
        for i in range(100):
            self.clock.set(self.periodsize * i, self.periodsize)
            target *= 0
            self.sched.render(target)
            stream_out.extend(target)
        stream_out = numarray.array(stream_out, type=numarray.Int16)
        
        pre_write = stream_out[:sound_start]
        self.assertEqual(numarray.any(pre_write), False)

        written = stream_out[sound_start:sound_stop]
        self.assertEqual(numarray.all(written), True)

        post_write = stream_out[sound_stop:]
        self.assertEqual(bool(numarray.any(post_write)), False)

    def test_write_many(self):
        starts = [200, 250, 300]        
        for frame in starts:
            self.sched.add(frame)

        predicted = buffering.Sound(10 * self.periodsize)
        for i in starts:
            predicted[i:i+len(self.sound)] += self.sound
        predicted = list(predicted)
            
        stream_out = []
        chunk = buffering.Sound(self.periodsize)
        for i in range(10):
            self.clock.set(self.periodsize * i, self.periodsize)
            chunk *= 0
            self.sched.render(chunk)
            stream_out.extend(chunk)

        self.assertEqual(predicted, stream_out)
        self.assertEqual(numarray.any(stream_out[:200]), False)
        self.assertEqual(numarray.any(stream_out[450:]), False)

    def _test_load_write_many(self):
        """ write many randomized notes. """
        def pending():
            return [e[0] for e in self.sched.pending]
        frames = [random.randint(0, len(self.sound)) for i in range(100)]
        for frame in frames:
            self.sched.add(frame)
        self.assertEqual(pending(), frames)

        stream_out = []
        chunk = buffering.Sound(1)
        for i in range(100 + len(self.sound)):
            self.clock.set(i, 1)
            self.sched.render(chunk)
            stream_out.extend(chunk)
        stream_out = buffering.Sound(seq=stream_out)
        predicted = buffering.Sound(len(stream_out))
        for i in frames:
            predicted[i:i+len(self.sound)] += self.sound
        self.assertEqual(stream_out, predicted)

    def test_recycle(self):
        sound = buffering.Sound(100)
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(self.sched.pending, [])
        self.assertEqual(self.sched.cache, [])

        self.sched.add(100)
        
        self.clock.set(0, 100)
        self.sched.render(sound)
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(len(self.sched.pending), 1)
        self.assertEqual(self.sched.cache, [])
        
        self.clock.set(100, 100)
        self.sched.render(sound)
        self.assertEqual(len(self.sched.rolling), 1)
        self.assertEqual(self.sched.pending, [])
        self.assertEqual(self.sched.cache, [])

        self.clock.set(200, 100)
        self.sched.render(sound)
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(self.sched.pending, [])
        self.assertEqual(len(self.sched.cache), 1)
        
        self.sched.add(400)
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(len(self.sched.pending), 1)
        self.assertEqual(self.sched.cache, [])
        
        self.clock.set(300, 100)
        self.sched.render(sound)
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(len(self.sched.pending), 1)
        self.assertEqual(self.sched.cache, [])

        self.clock.set(400, 100)
        self.sched.render(sound)
        self.assertEqual(len(self.sched.rolling), 1)
        self.assertEqual(self.sched.pending, [])
        self.assertEqual(self.sched.cache, [])

        self.clock.set(500, 100)
        self.sched.render(sound) # 500
        self.assertEqual(self.sched.rolling, [])
        self.assertEqual(self.sched.pending, [])
        self.assertEqual(len(self.sched.cache), 1)

    def _test_write_one_pitched(self):
        rf = ratefilter.RateFilter()
        rf.in_hz = self.sound.samplerate
        rf.out_hz = int(rf.in_hz * 2.0)
        rf.write(self.sound)
        sound = rf.read(rf.readable())

        self.sched.add(50)

        chunk = buffering.Sound(10)
        self.sched.pitch = 2.0
        stream_out = []
        for i in range(50):
            self.clock.set(i*10, 10)
            chunk *= 0
            self.sched.render(chunk)
            stream_out.extend(chunk)
        stream_out = buffering.Sound(seq=stream_out)

        predicted = buffering.Sound(len(stream_out))
        dest = predicted[50:50+len(sound)]
        orig = sound
        dest += orig

        self.assertEqual(numarray.any(predicted[:50]), False)
        self.assertEqual(numarray.any(predicted[50:]), True)
        self.assertEqual(numarray.any(stream_out[:50]), False)
        self.assertEqual(numarray.any(stream_out[50:]), True)
        self.assertEqual(len(stream_out), len(predicted))
        #self.assertEqual(stream_out, predicted)

    def _test_write_pitched(self):
        self.sched.pitch = 2.0
        rf = ratefilter.RateFilter()
        rf.in_hz = self.sound.samplerate
        rf.out_hz = int(rf.in_hz * 2.0)
        rf.write(self.sound)
        pitched_sound = rf.read(rf.readable())

        frames = [200]
        for i in frames:
            self.sched.add(i)

        stream_out = []
        chunk = buffering.Sound(1)
        length = 200 + len(pitched_sound)
        for i in range(length):
            chunk *= 0
            self.clock.set(i, 1)
            self.sched.render(chunk)
            stream_out.extend(chunk)
        stream_out = buffering.Sound(seq=stream_out)

        predicted = buffering.Sound(len(stream_out))
        for i in frames:
            x, y = i, i+len(pitched_sound)
            dest = predicted[x:y]
            dest += pitched_sound

        self.assertEqual(numarray.any(stream_out[:200]), False)
        self.assertEqual(numarray.any(predicted[:200]), False)
        self.assertEqual(predicted[200:], pitched_sound)
        self.assertEqual(stream_out[200:], pitched_sound)
        #self.assertEqual(stream_out, predicted)

    def _test_pitchslide(self):
        # oh man...
        pass


if __name__ == '__main__':
    scheduler.RESAMPLE = False
    unittest.main()

