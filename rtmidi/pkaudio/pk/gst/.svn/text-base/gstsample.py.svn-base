"""
Sample implementation for gstreamer.

NOTES:

To make a state change:
- bin.set_state(PAUSED) (cue buffer)
- bin.get_bus().poll(msgtypes)
    - watch FOR:
    GST_MESSAGE_ERROR
    GST_MESSAGE_EOS
    GST_MESSAGE_STATE_CHANGED
    ** STATES:
        GST_STATE_PENDING
        GST_STATE_CLOCK_PROVIDE
        GST_STATE_CLOCK
- handle message accordingly
- bin.set_state(PLAYING) (start rolling)
- periodically check for new messages.

IRC:

#gstreamer: bilboed (python examples), gnonlin
            wtay (internals expert)
            ensonic (buzztard, timing expert)

ENSONIC ON MUSIC TIMING/LOOPING:
For that you want to use segmented-seeks, you send a seek from current to the end-time, when end-time is reached you will receive an event, where you can restart src1 (loop) and also start the new source. If you know the bpm, you can send small segemnted seeks (they will be
continous) with the length of a beat. with a segmented seek you ask
the pipeline to play that segment of the stream (start-time to
end-time). If the segments are one after the other, they wont cause a
lot of overhead, but the give you control back from time to time

<ensonic> patrickkidd, imagine you have an own sink which also is a source and call that element sampler
<ensonic> patrickkidd, in a pieline you use one sampler per track
<ensonic> patrickkidd, the sampler itself is a bit like playbin, it has all element needed to play a file
<ensonic> patrickkidd, but as it is an own element you can have additional API, like enque_new_sample_for_timestamp()
<ensonic> patrickkidd, the element will open the sample, it will send out silence until playback reaches the timestamp and the
<ensonic> patrickkidd, the problem in gstreamer is that its diificult right now to start, stop elements on time, yright now one basically configures a pipeline and stars everything, then wait fot the pipeline to finish and eventually start the next one.


BIBLOED ON GNONLIN MUSIC TIMING:
<bilboed> patrickkidd, you just need 2 objects to start doing funky stuff.
          a gnlcomposition (which contains sources and orders them through
          time) and a gnlfilesource (which does the time-shifting of a source)
<bilboed> s/objects/gstelements/
<bilboed> let's start with the easiest, the gnlcomposition.             [23:20]
<bilboed> You don't need to set any properties on it if it's your
          top-level composition
<bilboed> the only thing you want is connect to the 'pad-added' signal and
          connect it to the rest of your pipeline (which can just be queue !
          alsasink for example) when the signal is fired
<bilboed> in that composition you're going to put some gnlfilesource    [23:22]
<bilboed> The important properties to set on a gnlfilesource are:
<bilboed> location (not a URI !, a full path location, ex :
          /the/path/leading/to/my/file.mp3)
<bilboed> caps , if your file contains more than one stream, you need to
          specify a caps matching what you want
          (ex : "audio/x-raw-int;audio/x-raw-float" if you want the audio
          stream from an audio/video file)
<bilboed> start, the position of your source in it's container
          (the OUTSIDE position)
<bilboed> duration, the duration of your source in it's container
          (the OUTSIDE duration)
<bilboed> media-start, the position you wish to start from IN your source
          (if you put 2*gst.SECOND, it will start playing from the 2nd
          second of your source)
<bilboed> media-duration, the duration you wish to use from your source
          (most of the time, the same as duration)
<bilboed> And of course, don't forget to add it to the gnlcomposition
<bilboed> and then the gnlcomposition behaves just like any other source
          gstreamer element (states, seek, query, ...)
<bilboed> patrickkidd, got all of that ?
<bilboed> patrickkidd, hint : if you want to debug what's going on in gnonlin
          objects, use GST_DEBUG=gnl*:5
<bilboed> patrickkidd, hint2 : you can use gstreamer debugging within your
          python program, and the debug category will be python (ex :
          GST_DEBUG=python:5)

<bilboed> patrickkidd, I need to add some gnllivesource elements
<bilboed> patrickkidd, the only thing to do would be different overrides for
          events
<bilboed> patrickkidd, for NEWSEGMENT and SEEK I guess
<bilboed> in fact, just NEWSEGMENT
<bilboed> patrickkidd, and I guess modifying the live gst source elements so
          they can handle segment seeks (and stop after X seconds of playback)
<bilboed> patrickkidd, gnonlin is only about time-shifting, welcome to the
          realm of time segments :)


AMAROK:
GstEngine uses following pipeline for playing (syntax used by gst-launch):
{ filesrc location=file.ext ! decodebin ! audioconvert ! audioscale ! volume
! adder } ! { queue ! equalizer ! identity ! volume ! audiosink }

look in amarok/engine/gst for a comprehesive qt/gtk example.

EXAMPLES:

http://cvs.freedesktop.org/gstreamer/gst-plugins-base/tests/examples/seek/
http://cvs.freedesktop.org/gstreamer/gstreamer/tests/examples/controller/

"""

import time
import gst
from PyQt4.QtCore import QObject, SIGNAL
import stub
from qgstobject import QGstObject


class LevelBus(QObject):
    def __init__(self, gst_level, parent=None):
        QObject.__init__(self, parent)
        self.gst_level = gst_level
        # something like this?
        #self.level.set_property('message', on)
        #self.gst_level.connect('message', self.cb_level)

        self.levels = {'peak' : [],
                       'rms' : [],
                       'decay' : [],
                       'endtime' : 0 }

    def gstEvent(self, e):
        if e.msg.src == self.level:
            if e.msg.type == gst.MESSAGE_STATE_CHANGED:
                return False

            # decode the message
            mlevels = {}
            for k in e.msg.structure.keys():
                mlevels[k] = e.msg.structure[k]

            # encode for LevelBus
            channels = len(levels['rms'])
            ret = {}
            for i in range(channels):
                for key in ('rms', 'decay', 'peak'):
                    key = self.normalize(mlevels[key][i])
                    ret[key].append(value)
            self.set(ret['rms'], ret['peak'], ret['decay'])
            
            e.accept()
            return True
        else:
            return False

    def set_interval(self, ms):
        self.level.set_property('interval', ms * 1000000)

    def normalize(self, db):
        """ 0.0 <= x <= 1.0 """
        return pow(10, db / 20)



class Sample(QGstObject, stub.Sample):

    buffer_time = -1
    latency_time = -1
    
    def __init__(self):
        self.bin = gst.parse_launch('filesrc name=source ! ' +
                                    'decodebin name=decodebin ! ' +
                                    'audioconvert ! ' +
                                    'volume name=volume ! ' +
                                    'speed name=speed ! ' +
                                    'audioresample ! ' +
                                    'level name=level ! ' +
                                    'alsasink name=alsasink')
        self.filesrc = self.bin.get_by_name('source')
        self.decodebin = self.bin.get_by_name('decodebin')
        self.speed = self.bin.get_by_name('speed')
        self.volume = self.bin.get_by_name('volume')
        self.audioresample = self.bin.get_by_name('audioresample')
        self.alsasink = self.bin.get_by_name('alsasink')
        
        self.alsasink.set_property('buffer-time', self.buffer_time)
        self.alsasink.set_property('latency-time', self.latency_time)
        
        self.level = self.bin.get_by_name('level')
        stub.Sample.__init__(self)
        self.levelbus = LevelBus(self.level, self)
        QGstObject.__init__(self, self.bin)
        self.is_playing = False

        bus = self.bin.get_bus()
        bus.connect('message::new-clock', self.cb_message)
        bus.connect('message::error', self.cb_message)
        bus.connect('message::message', self.cb_message)
        bus.connect('message::eos', self.cb_message)
        bus.connect('message::segment-done', self.cb_message)
        bus.connect('message::segment-done', self.cb_segment_done)

# this is causing abort() for some reason
#        self.decodebin.connect('new-decoded-pad', self.cb_new_decode_pad)
#
#    def cb_new_decode_pad(self, decodebin, pad, is_last):
#        caps = pad.get_caps().to_string()
#        if not 'audio' in caps:
#            return
#        dest_pad = self.speed.get_pad('sink')
#        if not dest_pad.is_linked():
#            pad.link(dest_pad)

    def gstEvent(self, e):
        if e.msg.src == self.level:
            if e.msg.type == gst.MESSAGE_STATE_CHANGED:
                return False
            self.levels = {}
            for k in e.msg.structure.keys():
                self.levels[k] = e.msg.structure[k]
            self.emit(SIGNAL('levelsUpdated()'))
            e.accept()
            return True
        else:
            return False

    def load(self, fpath):
        self.filesrc.set_property('location', fpath)
        self.change_state(gst.STATE_PAUSED)

    def play(self):
        self.change_state(gst.STATE_PLAYING)
        self.is_playing = True

    def pause(self):
        self.change_state(gst.STATE_PAUSED)
        self.is_playing = False

    def set_pitch(self, pitch):
        self.speed.set_property('speed', pitch)

    def set_volume(self, vol):
        self.volume.set_property('volume', vol)

    def should_loop(self, on):
        self.looping = on

    def loop_now(self):
        self.should_loop(True)
        seek = gst.event_new_seek(1.0,
                                  gst.FORMAT_TIME,
                                  gst.SEEK_FLAG_SEGMENT,
                                  gst.SEEK_TYPE_SET, 0,
                                  gst.SEEK_TYPE_NONE, 0)

    def cb_segment_done(self, msg, pipeline):
        print 'cb_segment_done', msg, pipeline
                                  
    def cb_message(self, msg, pipeline):
        #print 'cb_message', msg, pipeline
        pass




def main():
    import time
    import sys
    from PyQt4.QtGui import QObject, SIGNAL
    from PyQt4.QtCore import QApplication, QPushButton
    
    if len(sys.argv) != 2:
        print 'Usage: %s <file>' % sys.argv[0]
        sys.exit(0)
    else:
        uri = sys.argv[1]

    app = QApplication(sys.argv)
    w = QPushButton('exit')
    w.show()
    QObject.connect(w, SIGNAL('clicked()'), app.quit)
    sample = Sample()
    sample.load(uri)
    sample.play()
    app.exec_()


if __name__ == '__main__':
    main()
