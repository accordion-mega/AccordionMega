#   Copyright (C) 2006 by Patrick Stinson                                 
#   patrickkidd@gmail.com                                                   
#                                                                         
#   This program is free software; you can redistribute it and/or modify  
#   it under the terms of the GNU General Public License as published by  
#   the Free Software Foundation; either version 2 of the License, or     
#   (at your option) any later version.                                   
#                                                                         
#   This program is distributed in the hope that it will be useful,       
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#   GNU General Public License for more details.                          
#                                                                         
#   You should have received a copy of the GNU General Public License     
#   along with this program; if not, write to the                         
#   Free Software Foundation, Inc.,                                       
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  
#
"""
pksampler | supercollider
"""

import time
from PyQt4.QtCore import QObject, SIGNAL, QThread
import scsynth
import threading


Note = scsynth.Note

class Pattern(QObject, scsynth.Pattern):
    """ playing pattern """

    def __init__(self, beats=4, parent=None):
        QObject.__init__(self, parent)
        scsynth.Pattern.__init__(self, beats=beats)


class Engine(QObject, threading.Thread):
    """ App-level music interface.

    ControlLoop
        inputs: pattern, next_beat, time.time()
        outputs: notes, abs_times

    Emitter
        stream status
        levels?    
    """
    
    def __init__(self, server, parent=None, verbose=False, spew=False,
                 quit_on_delete=False):
        QObject.__init__(self, parent)
        threading.Thread.__init__(self)
        self.server = server
        self.tempoclock = scsynth.TempoClock(140)
        self.player = scsynth.Player(self.server)
        self.loader = scsynth.Loader(self.server)
        self.window = scsynth.Window(self.tempoclock)
        self.sequencer = scsynth.Sequencer(self.tempoclock)
        self._timer = None
        self.running = True
        self.quit_on_delete = quit_on_delete
        self.streams = []

    def __del__(self):
        if self.quit_on_delete:
            self.stop()
            self.server.quit()

    # event loop

    def stop(self):
        if self.isAlive():
            self.running = False
            self.join()

    def run(self):
        self.running = True
        while self.running:
            self.process()
            # twiddle this value
            self.window.length = self.tempoclock.spb() / 64.0
            time.sleep(self.window.length)

    def process(self):
        """ Process the time window, then adjust the beginning. """
        self.window.update()
        for stream, start, stop, pitch in self.sequencer.render(self.window):
            synth = stream.pattern.synth
            if not synth is None:
                synth.pitch(pitch)
                self.player.play(synth, start, stop)
                synth.add_note(start, stop) # NEW
        self.window.close()

    def timerEvent(self, e):
        self.update_gui()

    def update_gui(self):
        """ emit app status signals. """
        for stream in self.streams:
            stream.pattern.emit(SIGNAL('readCursor(int)'),
                                stream.cursor % (stream.pattern.beats * 64))
            if stream.pattern.synth:
                stream.pattern.synth.update()

    # public access

    def start(self, lead=None, length=None):
        if not self._timer is None:
            self.killTimer(self._timer)
        if lead:
            self.window.lead = lead
        if length:
            self.window.length = length
        self._timer = self.startTimer(self.window.length * 1000)
        threading.Thread.start(self)

    def insert(self, pattern):
        # bad!
        stream = self.sequencer.add(pattern)
        self.streams.append(stream)
        return stream

    def remove(self, pattern):
        for stream in self.streams:
            if stream.pattern == pattern:
                pattern.emit(SIGNAL('cursor(int)'), 0)
                if pattern.synth:
                    pattern.synth.clear_notes()
                    pattern.synth.update()
                self.streams.remove(stream)
                self.sequencer.remove(stream.pattern)


def metronome():
    import os, sys, time
    from PyQt4.QtCore import SIGNAL
    from PyQt4.QtGui import QApplication, QPushButton, QSlider, QWidget
    from PyQt4.QtGui import QHBoxLayout, QLabel
    import synths

    START = False
    
    app = QApplication(sys.argv)
    if START:
        server = scsynth.server.start(verbose=True, spew=True)
    else:
        server = scsynth.server.connect(verbose=True, spew=True)
    engine = Engine(server, app, spew=True, quit_on_delete=START)
    server.sendMsg('/dumpOSC', 1)
    engine.tempoclock.set_tempo(120)

    SYNTHDEF_PATH = os.path.join(os.path.expanduser('~'),
                                 '.pksampler', 'synthdefs')
    SYNTHDEFS = ('JASStereoSamplePlayer.scsyndef',
                 'JASSine.scsyndef',
                 )
    for fname in SYNTHDEFS:
        engine.server.sendMsg('/d_load', os.path.join(SYNTHDEF_PATH, fname))
    
    FPATH = '/Users/patrick/.pksampler/clicks/click_1.wav'
    click = synths.Synth()
    click.name = 'JASStereoSamplePlayer'
    click['bufnum'] = engine.loader.load(FPATH)
    click['rateSCale'] = 1.2
    click['loopIt'] = 0
    time.sleep(.1)

    pattern = Pattern(beats=1)
    pattern.add(Note(0, 64, 69))
    pattern.synth = click
    stream = engine.insert(pattern)
    stream.loop(True)

    widget = QWidget()
    Layout = QHBoxLayout(widget)
    widget.resize(100, 250)
    widget.show()

    label = QLabel(widget)
    label.setText(str(engine.tempoclock.bpm))
    Layout.addWidget(label)
    
    def set_tempo(value):
        engine.tempoclock.set_tempo(value)
        label.setText(str(value))

    slider = QSlider(widget)
    slider.setRange(100, 180)
    slider.setValue(140)
    QObject.connect(slider, SIGNAL('valueChanged(int)'), set_tempo)
    Layout.addWidget(slider)

    button = QPushButton('quit', widget)
    QObject.connect(button, SIGNAL('clicked()'), app.quit)
    Layout.addWidget(button)

    engine.start()
    app.exec_()
    engine.stop()


if __name__ == '__main__':
    metronome()
