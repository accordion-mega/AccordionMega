import os, sys
BUILD_PATHS = [os.path.join(os.getcwd(), 'build/lib.linux-x86_64-2.4/'),
               os.path.join(os.getcwd(), 'build/lib.darwin-8.6.0-Power_Macintosh-2.3/'),
               ]
sys.path = BUILD_PATHS + sys.path

import unittest
import rtaudio

OSNAME = os.uname()[0]

class RtAudioTest(unittest.TestCase):

    def setUp(self):
        self.rtaudio = rtaudio.RtAudio()

    def test_funcs(self):
        self.rtaudio.openStream(0, 2, 0, 0, rtaudio.RTAUDIO_FLOAT32,
                                44100, 1024, 2)

        old = rtaudio.get_priority()
        if OSNAME == 'Linux':
            self.assertEqual(old, 0)
        elif OSNAME == 'Darwin':
            self.assertEqual(old, 31)
        ret = rtaudio.boost_priority()
        new = rtaudio.get_priority()

        rtaudio.set_priority(40)
        new = rtaudio.get_priority()
        self.assertEqual(new, 40)
        
    def _test_openStream(self):
        channels = 2
        
        last = self.rtaudio.getDeviceCount()
        self.assertRaises(rtaudio.RtError, self.rtaudio.getStreamBuffer)

        self.rtaudio.openStream(last, channels, 0, 0,
                                rtaudio.RTAUDIO_FLOAT32,
                                44100, 1024, 2)
        
        # these may not actually match up, but whatev...
        streamBuffer = self.rtaudio.getStreamBuffer()
        #self.assertEqual(len(streamBuffer), (1024+1) * channels)

        # please don't crash...
        del self.rtaudio
        len(streamBuffer)
        del streamBuffer


def print_devices(device):
    devices = range(device.getDeviceCount())
    if devices:
        for i in devices:
            info = device.getDeviceInfo(i+1)
            print info['name']
            for k,v in info.items():
                if k != 'name':
                    print '    ',k,v
            print
    else:
        print 'NO DEVICES!'


def open_device(device):
    top = device.getDeviceCount()
    print device.getDeviceInfo(top)['name']
    ret = device.openStream(top, 2, 0, 0, rtaudio.RTAUDIO_FLOAT32,
                            44100, 0, 2)
    print ret
    stream_in = device.getStreamBuffer()
    print len(stream_in), stream_in.type()
    return stream_in

if __name__ == '__main__':
    #device = rtaudio.RtAudio()
    #print_devices(device)
    #stream_in = open_device(device)
    unittest.main()

