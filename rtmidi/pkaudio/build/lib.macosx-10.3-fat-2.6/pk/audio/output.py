"""
Platform wrappers.
"""

import os
import sys
import atexit
import time
import numarray # we use numarray in this house
import thread


USE_RTAUDIO = True
USE_NULL = False

if '--null' in sys.argv:
    USE_NULL = True
    USE_RTAUDIO = False


def runit(name, it):
    '''Run a function in a thread'''
    thd_it = threading.Thread(name=name, target=it)
    thd_it.setDaemon(True) # die event if running
    thd_it.start()
    return thd_it


def short16_to_float32(buffer):
    return buffer.astype(numarray.Float32) / 32768.0


def float32_to_short16(chunk):
    return (chunk * 32768).astype(numarray.Int16)


class SimpleOutput:
    """ very juvenile do-everything class """

    periodsize = 512
    samplerate = 44100
    _running = False
    _thread = None
    _usage = 0.0
    _start = 0.0
    _stop = 0.0
    frame_time = 0

    def __init__(self):
        pass

    def __del__(self):
        self.stop()

    def _fake_thread(self):
        self._running = True
        self._fake_buffer = numarray.array((0.0,) * self.periodsize,
                                           numarray.Float32)
        ms = self.periodsize / float(self.samplerate)
        while self._running:
            self.start_period()
            time.sleep(ms)
            self._fake_buffer *= 0
            self.render(self._fake_buffer)
            self.frame_time += self.periodsize
            self.stop_period()

    def init(self):
        pass

    def start(self):
        self._thread = thread.start_new_thread(self._fake_thread, ())

    def stop(self):
        self._running = False

    def cpu_load(self):
        return self._usage

    def render(self, out_array):
        pass

    def start_period(self):
        self.inv_micros = self.samplerate / (1000000.0 * self.periodsize * 2)
        self._start = time.time()
        
    def stop_period(self):
        self._stop = time.time()
        usecs = self._start - self._stop
        self._usage = usecs * self.inv_micros * -1


##############################################################################
## RtAudio: the waaave the future!


def init_RtAudio():
    try:
        import rtaudio
    except ImportError, e:
        print e
        print ' ** Could not start pkaudio engine.'
        print '    Does some other app have the audio device?'


class RtAudioOutput(SimpleOutput):

    def __init__(self, type=numarray.Float32):
        import rtaudio
        SimpleOutput.__init__(self)
        self.rtaudio = rtaudio.RtAudio()
        self.frame_time = 0
        self.type = type
        self.running = False

    def _get_rt(self, priority=None):
        import rtaudio
        try:
            rtaudio.boost_priority()
            old = rtaudio.get_priority()
            if priority != None:
                rtaudio.set_priority(priority)
            new = rtaudio.get_priority()
            if old != None and new != None:
                print 'PRIORITY: old %i, new %i' % (old, new)
        except rtaudio.RtError, e:
            pass
        return rtaudio.get_priority()

    def init(self):
        import rtaudio
        if self.type == numarray.Int16:
            type = rtaudio.RTAUDIO_SINT16
        else:
            type = rtaudio.RTAUDIO_FLOAT32
        self.rtaudio.openStream(0, 2, 0, 0,
                                type,
                                self.samplerate, self.periodsize / 2, 2)
        self.streamBuffer = self.rtaudio.getStreamBuffer()
        self.rtaudio.startStream()

    def start(self):
        self.init()
        thread.start_new_thread(self.run, ())

    def stop(self):
        if self._running:
            self.rtaudio.stopStream()
            self._running = False

    def run(self):
        self._get_rt(99)
        self._running = True
        while self._running:
            self.start_period()
            self.frame_time += self.periodsize / 2
            self.streamBuffer *= 0
            self.render(self.streamBuffer)
            self.rtaudio.tickStream()
            self.stop_period()


##############################################################################
## portaudio (Lee-nux) should only use this if its easy to install


def init_PortAudio():
    try:
        import dsptools.portaudio as pa
        pa.initialize()
    except Exception, e:
        print e
        print ' ** Could not start pkaudio engine.'
        print '    Does some other app have the audio device?'


def teardown_PortAudio():
    #import dsptools.portaudio as pa
    #pa.terminate()
    pass


class PortAudioOutput(SimpleOutput):

    def __init__(self):
        SimpleOutput.__init__(self)
        self.stream = None
        self.frame_time = 0
        self._last_start = time.time()
        self._perioddiff = 1000
        self._periodtime = 0

    def cb_audio( self, in_array, out_array, fpb, frame_time, data ):
        self.frame_time = int(frame_time)
        
        start = time.time()
        self.render(out_array)
        end = time.time()

        self._perioddiff = (start - self._last_start)
        self._periodtime = (end - start)
        self._last_start = start
        return 0

    def init(self):
        import dsptools.portaudio as pa
        self.stream = pa.Stream(input_device = None,
                                output_sample_format = pa.Int16,
                                num_output_channels = 2,
                                output_device = 0,
                                callback = self.cb_audio,
                                frames_per_buffer = self.periodsize / 2,
                                sample_rate=self.samplerate)

    def start(self):
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
        else:
            raise RuntimeError('Stream not started')

    def cpu_load(self):
        if self.stream:
            return self.stream.get_cpu_load()
        else:
            return SimpleOutput.cpu_load(self)


##############################################################################
## Mac OS X support


def init_Darwin():
    import thread
    import coreaudio
    
    ## Have to initialize the threading mechanisms in order for
    ## PyGIL_Ensure to work
    thread.start_new_thread(lambda: None, ())


class CoreAudioOutput(SimpleOutput):
    
    def __init__(self):
        SimpleOutput.__init__(self)
        self.chunk = None
        self.frame_time = 0
        self.playing = False
        
    def callback(self):
        self.frame_time += self.periodsize
        self.chunk *= 0
        try: # coreaudio.so doesn't help much here
            self.render(self.chunk)
        except:
            exc = sys.exc_info()
            print '%s : %s' % (exc[0], exc[1])
        return self.chunk

    def init(self):
        self.periodsize = 512
        self.samplerate = 44100
        self.chunk = numarray.array([0] * self.periodsize,
                                    type=numarray.Float32)
        self.playing = True

    def start(self):
        self.init()
        import coreaudio
        coreaudio.installAudioCallback(self,
                                       rate=self.samplerate,
                                       bufsize=self.periodsize,
                                       debug=False)

    def stop(self):
        import coreaudio
        if self.playing is True:
            coreaudio.stopAudio(self)
            self.playing = False
        

OSNAME = hasattr(os, 'uname') and os.uname()[0] or 'Windows'

if USE_NULL:
    Output = SimpleOutput

elif USE_RTAUDIO:
    init_RtAudio()
    Output = RtAudioOutput

else:    
    if OSNAME == 'Darwin':
        init_Darwin()
        Output = CoreAudioOutput
        
    elif OSNAME == 'Linux':
        init_PortAudio()
        Output = PortAudioOutput
        atexit.register(teardown_PortAudio)

    else:
        Output = SimpleOutput
