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
Groups (synth, pattern), effects, volume
"""


from PyQt4.QtCore import QString, Qt, QPoint, QRect, SIGNAL, QMimeData, QObject
from PyQt4.QtGui import *
from pk.widgets.utils import POV_COLOR, h_centered
import pk.widgets
import pattern
import parts
import spec


class DropTarget(QWidget):

    margin = 3
    
    def __init__(self, mime, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedWidth(parts.WIDTH + self.margin * 2)
        self.setAutoFillBackground(True)
        self.palette().setColor(self.backgroundRole(),
                                POV_COLOR.light(150))
        self.setAcceptDrops(True)
        self.mime = mime
        self.parts = []
        self.active = True
        
    def dragEnterEvent(self, e):
        if e.mimeData().text() == self.mime:
            e.acceptProposedAction()

    def dropEvent(self, e):
        e.acceptProposedAction()
 
    def paintEvent(self, e):
        if self.active:
            painter = QPainter(self)
            pen = painter.pen()
            pen.setWidth(self.margin)
            pen.setColor(QColor('red').dark(150))
            painter.drawRect(0, 0, self.width(), self.height())

    def add(self, part):
        if isinstance(part.parent(), DropTarget):
            part.parent().remove(part)
        self.parts.append(part)
        QObject.connect(part, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        self._rearrange()

    def remove(self, part):
        self.parts.remove(part)
        QObject.disconnect(part, SIGNAL('selected(QWidget *)'),
                           self, SIGNAL('selected(QWidget *)'))
        self._rearrange()
        
    def _rearrange(self):
        y = self.margin
        for part in self.parts:
            part.setParent(self)
            part.show()
            part.move(self.margin, y)
            y += part.height()

    def setSlots(self, slots):
        self.setFixedHeight(slots * parts.HEIGHT + self.margin * 2)


class Channel(QFrame):

    SYNTH_SLOTS = 3
    EFFECT_SLOTS = 4
    SYNTH_HEIGHT = SYNTH_SLOTS * parts.HEIGHT + DropTarget.margin * 2
    EFFECT_HEIGHT = EFFECT_SLOTS * parts.HEIGHT + DropTarget.margin * 2
    HEIGHT = SYNTH_HEIGHT + EFFECT_HEIGHT # + 190
    selected = False
    
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QFrame.StyledPanel)
        self.palette().setColor(QPalette.Window, QColor(136, 136, 136))
        
        self.synthParent = DropTarget('SynthPart', self)
        self.synthParent.setSlots(self.SYNTH_SLOTS)
        self.effectParent = DropTarget('EffectPart', self)
        self.effectParent.setSlots(self.EFFECT_SLOTS)
        self.effectParent.hide()

        self.mixParent = QFrame(self)
        self.mixParent.setFrameShape(spec.FRAME_SHAPE)
        self.mixParent.setFixedSize(self.effectParent.size())
        self.volumeSlider = pk.widgets.MixerSlider(self.mixParent)
        
#        self.knobs = pk.widgets.Knobs(knobs=3, parent=self)
#        self.knobs.setFixedWidth(self.width()) 
#        self.panKnob = self.knobs.knobs[0]
#        QObject.connect(self.panKnob, SIGNAL('valueChanged(int)'),
#                        self.setVolume)
#        for index, knob in enumerate(self.knobs.knobs[1:]):
#            index += 1
#            setattr(self, 'send%iKnob' % index, knob)
#            send_slot = getattr(self, 'setSend%i' % index)
#            QObject.connect(knob, SIGNAL('valueChanged(int)'), send_slot)
       
        QObject.connect(self.synthParent, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        QObject.connect(self.effectParent, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        QObject.connect(self.volumeSlider, SIGNAL('valueChanged(int)'),
                        self.setVolume)

        self.setFixedSize(parts.WIDTH+8, self.HEIGHT)

        Layout = QVBoxLayout(self)
        Layout.setMargin(0)
        Layout.setSpacing(0)
        Layout.addWidget(self.synthParent)
        Layout.setStretchFactor(self.synthParent, self.SYNTH_SLOTS)
        Layout.addWidget(self.effectParent)
        Layout.setStretchFactor(self.effectParent, self.EFFECT_SLOTS)
        Layout.addWidget(self.mixParent)
        Layout.setStretchFactor(self.mixParent, self.EFFECT_SLOTS)
        MixLayout = QVBoxLayout(self.mixParent)
        h_centered(MixLayout, self.volumeSlider)

    def paintEvent(self, e):
        if self.selected:
            painter = QPainter(self)
            pen = painter.pen()
            pen.setWidth(self.margin)
            pen.setColor(QColor('red'))
            painter.drawRect(0, 0, self.width(), self.height())

    def mixMode(self):
        self.effectParent.hide()
        self.mixParent.show()

    def editMode(self):
        self.effectParent.show()
        self.mixParent.hide()

    def setVolume(self, midi):
        self.midiInput(0, 7, midi, 0)
        
    def midiInput(self, msg):
        channel, value1, value2, timestamp = msg
        if value1 == 7:
            self.volumeSlider.setValue(value2)
            self.emit(SIGNAL('volume(QWidget *, float)'), value2 / 127.0)
        elif value1 == 13:
            self.panKnob.setValue(value2)
        elif value1 == 12:
            self.send1Knob.setValue(value2)
        elif value1 == 10:
            self.send2Knob.setValue(value2)


if __name__ == '__main__':
    from pk.widgets.utils import run_widget
    import synths
    import effects
    import pattern
    import parts
    class TestChannel(Channel):
        def __init__(self):
            Channel.__init__(self)
            self.a = parts.SynthPart(synths.Sine())
            self.a.show()
            self.b = parts.EffectPart(effects.Effect(None))
            self.b.show()
            self.c = parts.PatternPart(pattern.Pattern())
            self.c.show()
    run_widget(TestChannel)
