"""
The idea here is to test if pkaudio can run on a given machine.
"""

import time
from pk.audio import scheduler
from pk.audio import buffering
from pk.audio import media
from pk.audio import flow
from pk.audio import instrument


BASE = os.path.join(os.environ['HOME'], 'wav/pksampler')
FNAMES = ('bass',
          #'drums',
          #'drums_bd',
          #'strings',
          #'sweeps',
          #'synth_waves',
          )
FPATHS = [os.path.join(BASE, fname+'.wav') for fname in FNAMES]


def Mixer():
    mixer = flow.Mixer()

    for fpath in FPATHS:
        sample = instrument.Instrument(mixer)
        sample.load(fpath)
        volume = flow.Volume()
        volume.volume = 0
        channel = flow.Channel([sample, volume])
        mixer.attach(channel)

    mixer.changeTempo(.1)
    mixer.start()
    mixer.channels[0][0].play()
    time.sleep(3)
    mixer.stop()


def Writer_resample():
    sound = buffering.Sound(1000)
    sound.write(media.RandomGenerator(1000).read(1000))
    writer = scheduler.Writer(sound)
    #writer.setpitch(1.0)

    chunk = buffering.Sound(100)
    for i in range(100):
        for i in range(3):
            writer.write(chunk)
        writer.reset()


def main():
    Writer_resample()
    Mixer()

import profile, pstats
profile.run('main()', 'tmp.profile')
s = pstats.Stats('tmp.profile')
s.sort_stats('module')
#s.strip_dirs()
#s.print_stats('ringbuffer.py:')
#s.print_stats('ratefilter.py:')
#s.print_stats('scheduler.py:')
s.print_stats('numarray')
s.print_stats('repos')
