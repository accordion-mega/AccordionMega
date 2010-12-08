import os
import sys
import fcntl
import Queue
import traceback
from pk.audio import flow
from pk.audio import instrument


_DEBUG = False
def DEBUG(msg):
    if _DEBUG:
        print msg


class MixerBase(flow.Mixer):
    def __init__(self):
        flow.Mixer.__init__(self)
        self.__instruments = {}
        self.__channels = {}
        
    def instrument(self, fpath):
        if not fpath in self.__instruments:
            self.__instruments[fpath] = instrument.Instrument(self)
        instr = self.__instruments[fpath]
        instr.load(fpath)
        return instr

    def channel(self, id):
        if not id in self.__channels:
            volume = flow.Volume()
            merger = flow.Merger()
            self.__channels[id] = flow.Channel([merger, volume])
            self.__channels[id].volume = volume
            self.__channels[id].merger = merger
            self.attach(self.__channels[id])
            print 'NEW CHANNEL:',id
        return self.__channels[id]

    def quit(self):
        self._running = False

    def load(self, fpath):
        self.instrument(fpath)

    def add_event(self, fpath, start, stop):
        self.instrument(fpath).play(start, None)

    def clear_events(self, fpath):
        self.instrument(fpath).stop()

    def add_to_channel(self, fpath, channel):
        instr = self.instrument(fpath)
        channel = self.channel(channel)
        channel.merger.attach(instr)

    def set_volume(self, channel, left, right):
        channel = self.channel(channel)
        if not left is None:
            channel.volume.left = left
        if not right is None:
            channel.volume.right = right

    def set_looping(self, fpath, on):
        self.instrument(fpath).loop(on)

    def set_tempo(self, tempo):
        flow.Mixer.set_tempo(self, tempo)

    def set_loop_beats(self, fpath, beats):
        self.instrument(fpath).setLoopBeats(beats)


class Server(MixerBase):

    def __init__(self, infile, outfile):
        MixerBase.__init__(self)
        fcntl.fcntl(infile, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(outfile, fcntl.F_SETFL, os.O_NONBLOCK)
        self.fd = infile.fileno()
        self.outfile = outfile # for the future
        self._buf = ''
        self.exec_ = self.run

    def parse_args(self, args):
        ret = ()
        for a in args:
            if a == 'None':
                a = None
            elif a == 'True':
                a = True
            elif a == 'False':
                a = False
            else:
                try:
                    a = int(a)
                except ValueError:
                    try:
                        a = float(a)
                    except ValueError:
                        pass
                except TypeError:
                    print type(a)
            ret += (a,)
        return ret
        
    def _handle(self, msg):
        DEBUG('MESSAGE: %s' % msg)
        parts = msg.split()
        if hasattr(self, parts[0]):
            func = getattr(self, parts[0])
        else:
            print msg
            return
        if len(parts) > 1:
            args = msg.split()[1:]
        else:
            args = ()
        args = self.parse_args(args)
        func(*args)

    def _poll(self):
        while True:
            try:
                ch = os.read(self.fd, 1)
                self._buf += ch
            except OSError, e:
                return False
            if ch == '\n' or ch == '\0':
                self._buf += ch
                msg = self._buf.replace('\n', '').replace('\0', '').strip()
                if msg:
                    self._handle(msg)
                self._buf = ''
                return False

    def run(self):
        try:
            return MixerBase.run(self)
        except:
            traceback.print_exc()


    def _check(self):
        while self._poll():
            pass

    def render(self, chunk):
        self._check()
        MixerBase.render(self, chunk)

    
if __name__ == '__main__':
    import sys
    import time
    server = Server(sys.stdin, sys.stdout)
    server.samplerate = 48000
    server._running = True
    server.init()
    server.run()
