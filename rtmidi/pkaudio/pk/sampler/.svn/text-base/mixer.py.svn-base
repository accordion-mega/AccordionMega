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
REQUIREMENTS
------------
 - channels: volume, pan, send1, send2
 - synths: start/stop
 - drag synths => channels
 - drag patterns => synths
 - drag effects => send1, send2
 - beat match tempo
 - settings:
   - mode: play,delete
"""

from pk.widgets import Button
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QFrame, QVBoxLayout, QGridLayout, QPainter, QColor, QHBoxLayout, QButtonGroup, QPalette
import pk.widgets
import pk.widgets.utils
import rtplayer
import controlpanel
import keyboard
import toolbox
import spec
import slots
import parts
import engine
import synths


LOOPS = 4


class ChannelControls(QFrame):
    """ Volume, knobs. """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setFrameShape(spec.FRAME_SHAPE)
        self.setFrameShadow(QFrame.Sunken)
        self.palette().setColor(self.backgroundRole(),
                                pk.widgets.utils.POV_COLOR)

        self.knobs = pk.widgets.Knobs(knobs=3, parent=self)
        self.send1Knob = self.knobs.knobs[0]
        self.send2Knob = self.knobs.knobs[1]
        self.panKnob = self.knobs.knobs[2]
        self.volumeSlider = pk.widgets.MixerSlider(self)
        self.volumeSlider.setRange(0, 127)
        self.volumeSlider.setValue(100)
        self.volumeSlider.animated = True

        QObject.connect(self.panKnob, SIGNAL('valueChanged(int)'),
                        self, SIGNAL('pan(int)'))
        QObject.connect(self.send1Knob, SIGNAL('valueChanged(int)'),
                        self, SIGNAL('send1(int)'))
        QObject.connect(self.send2Knob, SIGNAL('valueChanged(int)'),
                        self, SIGNAL('send2(int)'))
        QObject.connect(self.volumeSlider, SIGNAL('valueChanged(int)'),
                        self, SIGNAL('volume(int)'))

        Layout = QVBoxLayout(self)
        Layout.setSpacing(0)
        Layout.setMargin(0)
        pk.widgets.utils.h_centered(Layout, self.knobs)
        pk.widgets.utils.h_centered(Layout, self.volumeSlider)


class MainWindow(QFrame):
    def __init__(self, engine_, parent=None, channels=5):
        QFrame.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(self.backgroundRole(), spec.BACKGROUND)

        self.engine = engine_

        self.controlPanel = controlpanel.ControlPanel(self)
        self.keyboard = keyboard.Keyboard(self, orientation=Qt.Vertical)
        self.keyboard.keywidth = 25
        self.keyboard.setHalfSteps(127)
        self.keyboard.setMinimumWidth(50)

        self.channels = []
        synthpool = self.engine.server.synthpool
        buspool = self.engine.server.audiobuspool
        self.send1_bus = buspool.get()
        buspool.get()
        self.send2_bus = buspool.get()
        buspool.get()
        for i in range(channels):
            nid = synthpool.get()
            bus = buspool.get()
            buspool.get()
            self.engine.server.sendMsg('/s_new', 'JASBusDumpStereo', nid, 1, 0,
                                  'outBus', 0, 'inBus', bus)
            self.channels.append((nid, bus))
            
        self.controls = []
        MixerLayout = QHBoxLayout()
        for i in range(channels):
            ChannelLayout = QVBoxLayout()
            for j in range(LOOPS):
                loopzone = slots.SynthSlot(self)
                loopzone.frame_color = QColor('green')
                loopzone.frame_color.setAlpha(150)
                QObject.connect(loopzone,
                                SIGNAL('added(QWidget *, QWidget *)'),
                                self.loopAdded)
                QObject.connect(loopzone,
                                SIGNAL('deleted(QWidget *, QWidget *)'),
                                self.loopDeleted)
                QObject.connect(loopzone, SIGNAL('selected(QWidget *)'),
                                self.clicked)
                loopzone.index = i
                ChannelLayout.addWidget(loopzone)
            control = ChannelControls(self)
            control.index = i
            QObject.connect(control, SIGNAL('volume(int)'), self.slotVolume)
            ChannelLayout.addWidget(control)
            self.controls.append(control)
            MixerLayout.addLayout(ChannelLayout)

        self.toolbox = toolbox.ToolBox(self)
        self.toolbox.setFrameShape(spec.FRAME_SHAPE)
        self.toolbox.setFixedWidth(spec.PART_WIDTH + spec.SCROLLPAD_WIDTH + 10)

        self.rtplayer = rtplayer.RTPlayer(self.engine.server)
        self.rt_note = None
        self.current_synth = None
        self.mode = None
        self.set_mode('select')
        self.notes = {}
        self.send1_id = None
        self.clickStream = None
        self.clickSynth = synths.Sample()
        self.clickSynth['bufnum'] = None
        self.clickPattern = engine.Pattern(beats=1)
        self.clickPattern.add(engine.Note(0, 64, 69))
        self.clickPattern.synth = self.clickSynth

        QObject.connect(self.controlPanel.modeGroup,
                        SIGNAL('buttonClicked(QAbstractButton *)'),
                        self.mode_clicked)
        QObject.connect(self.keyboard,
                        SIGNAL('noteon(int, int)'),
                        self.noteon)
        QObject.connect(self.keyboard,
                        SIGNAL('noteoff(int, int)'),
                        self.noteoff)
        QObject.connect(self.controlPanel.clickButton, SIGNAL('clicked()'),
                        self.toggleClick)
        QObject.connect(self.toolbox.tempoAdjuster.bender,
                        SIGNAL('valueChanged(float)'),
                        self.engine.tempoclock.set_tempo)

        QObject.connect(self.controlPanel, SIGNAL('setSend1(QWidget *)'),
                        self.setSend1)
        QObject.connect(self.controlPanel, SIGNAL('setSend2(QWidget *)'),
                        self.setSend2)
        
        Layout = QVBoxLayout(self)
        Layout.addWidget(self.controlPanel)
        InnerLayout = QHBoxLayout()
        InnerLayout.addWidget(self.keyboard)
        InnerLayout.setStretchFactor(self.keyboard, 2)
        InnerLayout.addLayout(MixerLayout)
        InnerLayout.addWidget(self.toolbox)
        Layout.addLayout(InnerLayout)
        Layout.setStretchFactor(self.controlPanel, 0)
        Layout.setStretchFactor(InnerLayout, 2)

    def set_click(self, fpath):
        self.clickSynth['bufnum'] = self.engine.loader.load(fpath)

    def toggleClick(self, on=None):
        if on or self.clickStream is None:
            self.clickStream = self.engine.insert(self.clickPattern)
            self.clickStream.loop(True)
        elif self.clickStream:
            self.engine.remove(self.clickPattern)
            self.clickStream = None

    def loopAdded(self, part, slot):
        nid, bus = self.channels[slot.index]
        synth = part.data
        synth['bufnum'] = self.engine.loader.load(synth.filepath)
        synth['outBus'] = bus
        synth.node = nid

    def loopDeleted(self, part, slot):
        synth = part.data
        self.engine.loader.unload(synth['bufnum'])

    def setSend1(self, part):
        effect = part.data
        server = self.engine.server
        if not self.send1_id is None:
            server.sendMsg('/n_free', self.send1_id)
            server.synthpool.recycle(self.send1_id)
        self.send1_id = server.synthpool.get()
        server.sendMsg('/s_new', effect.name, self.send1_id, 1, 0,
                       'inBus', self.send1_bus)

    def setSend2(self, part):
        effect = part.data        

    def slotVolume(self, value):
        nid, bus = self.channels[self.sender().index]
        self.engine.server.sendMsg('/n_set', nid, 'amp', value / 100.0)

    def mode_clicked(self, button):
        self.set_mode(str(button.text()))

    def set_mode(self, mode):
        self.mode = mode
        getattr(self.controlPanel, mode+'Button').setChecked(True)

    def clicked(self, part):
        if self.current_synth:
            self.current_synth.set_selected(False)

        if self.mode == 'select':
            self.select(part)
        elif self.mode == 'delete':
            if part.stream:
                self.engine.remove(part.pattern)
            part.parent().remove(part)
            self.current_synth = None
            self.toolbox.loopSelector.add(part)
        elif self.mode == 'play':
            self.select(part)
            if part.stream:
                self.engine.remove(part.pattern)
                part.activate(False)
                part.stream = None
            elif part.pattern:
                synth = part.data
                if synth.filetempo:
                    ratio = self.engine.tempoclock.bpm / synth.filetempo
                    synth['rateSCale'] = ratio
                part.stream = self.engine.insert(part.pattern)
                part.activate(True)

    def select(self, part):
        part.set_selected(True)
        self.current_synth = part
        self.rtplayer.synth = part.data

    def noteon(self, note, vel):
        """ from editor keyboard """
        note -= 12 * 4
        if self.current_synth:
            synth = self.current_synth.data
            if synth.filetempo:
                ratio = self.engine.tempoclock.bpm / synth.filetempo
                synth['rateSCale'] = ratio
            synth.pitch(note)
            self.rt_note = self.engine.player.play_rt(synth)

    def noteoff(self, note, vel):
        """ from editor keyboard """
        if self.rt_note:
            self.engine.player.stop_rt(self.rt_note)
            self.rt_note = None

    def midi_note(self, msg):
        device, key, vel, timestamp = msg
        if vel:
            self.rtplayer.note_on(key, vel)
        else:
            self.rtplayer.note_off(key, vel)

    def midi_input(self, msg):
        # hard-coded for my UC-33e on the Reason Preset
        device, key, vel, timestamp = msg
        MAP = ((11, 19, 'volumeSlider'),
               (20, 27, 'panKnob'),
               (28, 35, 'send2Knob'),
               (36, 43, 'send1Knob'),
               )
        for min, max, name in MAP:
            if key >= min and key <= max:
                index = key - min
                try:
                    control = getattr(self.controls[index], name)
                    control.setValue(vel)
                except IndexError, e:
                    return
                return
