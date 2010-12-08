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
DJ Interface: straight line grasshopper, straight line...

Channels group volume, that's it
Global send1, send2
part click: start/stop
knobs: pan, send1, send2
drag synths
"""

import os.path
from PyQt4.QtCore import QObject, SIGNAL, QCoreApplication, QTimer, Qt
from PyQt4.QtGui import *
from pk.widgets.utils import POV_COLOR
import pk.widgets
import machine
import mixer
import patterneditor
import parts
import toolbox
import spec



class PlayerApp(QFrame):
    def __init__(self, engine, parent=None):
        QFrame.__init__(self)
        self.setAutoFillBackground(True)
        self.palette().setColor(QPalette.Window, spec.BACKGROUND)
    
        self.machine = machine.MachineControl(self)
        self.machine.setFrameShape(QFrame.WinPanel)
        self.machine.setFixedHeight(85)
        self.machine.setAutoFillBackground(True)
        self.machine.palette().setColor(self.machine.backgroundRole(),
                                        POV_COLOR)

        self.mixer = mixer.Mixer(self)
        self.mixerScrollArea = pk.widgets.ScrollArea(self,
                                                     color=spec.SCROLLPAD_COLOR)
        self.mixerScrollArea.setFrameShape(spec.FRAME_SHAPE)
        self.mixerScrollArea.setWidget(self.mixer)
        self.mixerScrollArea.horizontal(True)
        self.mixerScrollArea.vertical(False)
        self.mixerScrollArea.setMaximumHeight(mixer.Mixer.HEIGHT)
        self.mixerScrollArea.h_pad.setFixedHeight(spec.SCROLLPAD_WIDTH)

        self.editorContainer = QFrame(self)
        self.editorContainer.setFrameShape(spec.FRAME_SHAPE)
        self.patternEditor = patterneditor.PatternEditor(self.editorContainer)
        self.effectEditor = QLabel('EFFECT_EDITOR', self.editorContainer)
        self.effectEditor.setAlignment(Qt.AlignCenter)

        self.toolbox = toolbox.ToolBox(self)
        self.toolbox.setAutoFillBackground(True)
        self.toolbox.palette().setColor(self.toolbox.backgroundRole(),
                                        POV_COLOR)
        self.toolbox.setFrameShape(spec.FRAME_SHAPE)
        self.toolbox.setFixedWidth(parts.WIDTH + spec.SCROLLPAD_WIDTH + 10)

        QObject.connect(self.toolbox.tempoAdjuster, SIGNAL('tempo(float)'),
                        self.set_tempo)
        QObject.connect(self.mixer, SIGNAL('selected(QWidget *)'),
                        self.clicked)
        QObject.connect(self.machine.modeGroup,
                        SIGNAL('buttonClicked(QAbstractButton *)'),
                        self.mode_selected)
        QObject.connect(self.machine.metroButton, SIGNAL('toggled(bool)'),
                        self.toggleMetronome)
        QObject.connect(self.patternEditor.keyboard,
                        SIGNAL('noteon(int, int)'),
                        self.noteon)
        QObject.connect(self.patternEditor.keyboard,
                        SIGNAL('noteoff(int, int)'),
                        self.noteoff)

        # now I'm getting carried away. everything needs a re-design.
        QObject.connect(self.mixer, SIGNAL('volume(int, float)'),
                        self.channelVolume)
        
        for i in range(24): self.mixer.new()
        self.mapper = self.machine.inputMapper
        self.mapper.set_default(self.default_input)
        self.mapper.grabKeyboard()
        self.mapper.midiin.start()
        self.engine = engine
        self.current_part = None
        self.rt_note = None
        self.metro_stream = None
        self.set_mode('select')

        EditorLayout = QStackedLayout(self.editorContainer)
        EditorLayout.addWidget(self.patternEditor)
        EditorLayout.addWidget(self.effectEditor)
        self.editorStack = EditorLayout
        LeftLayout = QVBoxLayout()
        LeftLayout.addWidget(self.mixerScrollArea)
        LeftLayout.addWidget(self.editorContainer)
        MainLayout = QHBoxLayout()
        MainLayout.addLayout(LeftLayout)
        MainLayout.addWidget(self.toolbox)
        Layout = QVBoxLayout(self)
        Layout.setSpacing(7)
        Layout.addWidget(self.machine)
        Layout.addLayout(MainLayout)

    def default_input(self, msg=None):
        if isinstance(msg, tuple):
            channel, value1, value2, timestamp = msg

    def mode_selected(self, button):
        self.set_mode(str(button.text()))

    def grow_editor(self):
        """ this is only here because there is nothing else to take up
        the space left from a fixed mixer size.
        """
        self.mixerScrollArea.hide()
        return
        sp_height = self.mixerScrollArea.h_pad.height() + 3
        height = self.mixer.SYNTH_HEIGHT + sp_height        
        self.mixerScrollArea.setFixedHeight(height + 10)
        
    def shrink_editor(self):
        """ this is only here because there is nothing else to take up
        the space left from a fixed mixer size.
        """
        self.mixerScrollArea.show()
        sp_height = self.mixerScrollArea.h_pad.height() + 3
        height = self.mixer.HEIGHT + sp_height
        self.mixerScrollArea.setFixedHeight(height)

    def set_mode(self, mode):
        if mode == 'select':
            self.machine.selectButton.setChecked(True)
        elif mode == 'edit':
            self.machine.editButton.setChecked(True)
            if isinstance(self.current_part, parts.SynthPart):
                self.editorStack.setCurrentWidget(self.patternEditor)
            elif isinstance(self.current_part, parts.EffectPart):
                self.editorStack.setCurrentWidget(self.effectEditor)
            for channel in self.mixer.channels:
                channel.editMode()
        elif mode == 'delete':
            self.machine.deleteButton.setChecked(True)
        elif mode == 'play':
            self.machine.playButton.setChecked(True)
            for channel in self.mixer.channels:
                channel.mixMode()
        self.shrink_editor()
        self.mode = mode

    def select(self, part):
        if self.current_part:
            self.current_part.set_selected(False)
        if isinstance(self.current_part, parts.SynthPart):
            if self.current_part.stream:
                QObject.disconnect(self.current_part.stream,
                                   SIGNAL('cursor(int)'),
                                   self.patternEditor.grid.set_play_cursor)
            self.patternEditor.grid.set_play_cursor(0)
        elif isinstance(self.current_part, parts.EffectPart):
            pass

        self.current_part = part
        if isinstance(self.current_part, parts.SynthPart):
            if self.current_part.stream:
                QObject.connect(self.current_part.stream, SIGNAL('cursor(int)'),
                                self.patternEditor.grid.set_play_cursor)
            self.current_part.set_selected(True)
        elif isinstance(self.current_part, parts.EffectPart):
            self.current_part.set_selected(True)

    def synth_clicked(self, synthpart):
        if self.mode == 'select':
            self.select(synthpart)
        elif self.mode == 'play':
            if synthpart.stream:
                self.engine.deregister(synthpart.stream)
                synthpart.stream = None
                synthpart.activate(False)
            else:
                synthpart.stream = self.engine.register(synthpart.data,
                                                        synthpart.pattern)
                synthpart.activate(True)
            self.select(synthpart)
        elif self.mode == 'edit':
            self.select(synthpart)
            self.grow_editor()
        elif self.mode == 'delete':
            if synthpart.stream:
                self.engine.deregister(synthpart.stream)
            synthpart.parent().remove(synthpart)
            synthpart.setParent(None)
        self.patternEditor.set_pattern(synthpart.pattern)
        self.patternEditor.grid.set_play_cursor(0)
        self.editorStack.setCurrentWidget(self.patternEditor)

    def effect_clicked(self, effectpart):
        if self.mode == 'play':
            self.select(effectpart)
        elif self.mode == 'edit':
            self.select(effectpart)
            self.grow_editor()
        elif self.mode == 'delete':
            effectpart.parent().remove(effectpart)
            effectpart.setParent(None)
        self.patternEditor.grid.set_play_cursor(0)
        self.editorStack.setCurrentWidget(self.effectEditor)
        
    def clicked(self, part):
        if isinstance(part, parts.SynthPart):
            self.synth_clicked(part)
        elif isinstance(part, parts.EffectPart):
            self.effect_clicked(part)
        if self.mode == 'delete':
            self.current_part = None

    def set_tempo(self, tempo):
        self.toolbox.tempoAdjuster.set_tempo(tempo, emit=False)
        self.engine.set_tempo(tempo)

    def toggleMetronome(self, on):
        if on:
            self.metro_stream = self.engine.register(self.machine.click,
                                                     self.machine.steady)
        elif self.metro_stream:
            self.engine.deregister(self.metro_stream)
            self.metro_stream = None

    def set_click(self, fpath):
        wason = bool(self.metro_stream)
        self.toggleMetronome(False)
        self.machine.click['bufnum'] = self.engine.player.load(fpath)
        if wason:
            self.toggleMetronome(True)

    def noteon(self, note, vel):
        """ from editor keyboard """
        if isinstance(self.current_part, parts.SynthPart):
            synth = self.current_part.data.copy()
            synth.pitch(note)
            self.rt_note = self.engine.player.play_rt(synth)

    def noteoff(self, note, vel):
        """ from editor keyboard """
        if self.rt_note:
            self.engine.player.stop_rt(self.rt_note)
            self.rt_note = None


