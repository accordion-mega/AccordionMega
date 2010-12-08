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

from PyQt4.QtCore import QCoreApplication, QObject, SIGNAL, QThread, Qt
from PyQt4.QtGui import QApplication, QWidget, QLabel, QGridLayout
import rtmidi
import pk.widgets


class MidiInput(QThread):
    def __init__(self, devid, parent=None):
        QThread.__init__(self, parent)
        self.running = False
        try:
            self.device = rtmidi.RtMidiIn()
        except rtmidi.RtError, e:
            print 'Error polling midi input devices',e
            return
        
        if self.device.getPortCount() == 0:
            return

        try:
            self.device.openPort(devid, True)
            self.running = True
        except rtmidi.RtError, e:
            print 'Could not open MIDI device %i' % devid

    def run(self):
        while self.running:
            msg = self.device.getMessage()
            if msg:
                self.msg = msg
                self.emit(SIGNAL('midiMessage(PyObject *)'), self.msg)
                self.emit(SIGNAL('midiMessage()'))


class ControlMapper(QLabel):
    """ Grabs and maps all input. """
    def __init__(self, device, parent=None):
        QLabel.__init__(self, parent)
        self.controls = {}
        self.keys = {}

        self.midiin = MidiInput(0, self)
        QObject.connect(self.midiin, SIGNAL('midiMessage()'),
                        self._midi_message)

    def _midi_message(self):
        self.midiEvent(self.midiin.msg)

    def midiEvent(self, msg):
        channel = msg[0]
        self.controls.get(channel, self._default)(self.midiin.msg)

    def keyPressEvent(self, e):
        self.keys.get(e.key(), self._default)(e.key())

    def _default(self, msg=None):
        print 'UNBOUND MIDI:',msg

    def set_default(self, callback):
        self._default = callback

    def set_midi(self, channel, callback):
        self.controls[channel] = callback

    def set_key(self, key, callback):
        self.keys[key] = callback

    def clear_midi(self):
        self.controls = {}

    def clear_keys(self):
        self.keys = {}


class InputWidget(ControlMapper):
    def __init__(self, device=1, parent=None):
        ControlMapper.__init__(self, device, parent)

        self.midiLabel = QLabel('midi', self)
        self.midiLabel.setAlignment(Qt.AlignCenter)
        self.midiLED = pk.widgets.LED(self)
        self.midiLED.setFixedSize(20, 10)
        
        self.kbLabel = QLabel('kb', self)
        self.kbLabel.setAlignment(Qt.AlignCenter)
        self.kbLED = pk.widgets.LED(self)
        self.kbLED.setFixedSize(20, 10)

        Layout = QGridLayout(self)
        Layout.setRowStretch(0, 1)
        Layout.addWidget(self.kbLabel, 2, 0)
        Layout.addWidget(self.kbLED, 1, 0)
        Layout.addWidget(self.midiLabel, 2, 1)
        Layout.addWidget(self.midiLED, 1, 1)
        Layout.setRowStretch(3, 1)
        
    def midiEvent(self, msg):
        self.midiLED.blink()
        ControlMapper.midiEvent(self, msg)

    def keyPressEvent(self, e):
        self.kbLED.blink()
        ControlMapper.keyPressEvent(self, e)


def _main1():
    from PyQt4.QtGui import QApplication, QLabel
    app = QApplication([])
    label = QLabel('no message yet')
    mapper = InputWidget()
    
    def cb_message(msg):
        print 'message',msg
    def channel_180(msg):
        label.setText(str(msg))
        
    mapper.set_default(cb_message)
    mapper.set_midi(180, channel_180)
    mapper.midiin.start()
    mapper.show()
#    label.show()
    app.exec_()

def _main2():
    import time
    midiin = MidiInput(1)
    midiin.start()
    time.sleep(1)

if __name__ == '__main__':
    _main1()
    
