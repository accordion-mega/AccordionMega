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
Global-ish controls
"""

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QFrame, QHBoxLayout, QButtonGroup, QColor, QLabel, QGridLayout, QPalette, QApplication
import pk.widgets
import pk.widgets.utils
import midi
import spec
import slots


SLOT_COLOR = QColor(0, 0, 255, 150).light(115)


class QuitterLabel(QLabel):
    def mouseReleaseEvent(self, e):
        QApplication.instance().quit()


class ControlPanel(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameShape(spec.FRAME_SHAPE)
        self.setAutoFillBackground(True)
        self.palette().setColor(self.backgroundRole(),
                                spec.POV_COLOR)

        self.label = QuitterLabel('pksampler', self)
        self.label.setScaledContents(True)
        font = self.label.font()
        font.setPointSize(40)
        font.setFamily('Lucida Grande')
        self.label.palette().setColor(QPalette.WindowText, QColor(60, 60, 80))
        
        self.mapper = midi.InputWidget(parent=self)
        self.mapper.setMinimumHeight(50)
        self.mapper.setMinimumWidth(100)
        self.send1Slot = slots.EffectSlot(self)
        self.send1Slot.frame_color = SLOT_COLOR
        self.send2Slot = slots.EffectSlot(self)
        self.send2Slot.frame_color = SLOT_COLOR
        
        self.modeGroup = QButtonGroup(self)
        self.modeGroup.setExclusive(True)
        self.modeButtons = []
        for mode in ('select', 'play', 'delete'):
            button = pk.widgets.Button(self)
            button.setText(mode)
            button.setCheckable(True)
            setattr(self, mode+'Button', button)
            self.modeGroup.addButton(button)
            self.modeButtons.append(button)

        self.clickButton = pk.widgets.Button(self, color='green')
        self.clickButton.setText('click')
        self.clickButton.setCheckable(True)

        QObject.connect(self.send1Slot, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        QObject.connect(self.send2Slot, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        QObject.connect(self.send1Slot,
                        SIGNAL('added(QWidget *, QWidget *)'),
                        self.setSend)
        QObject.connect(self.send1Slot,
                        SIGNAL('deleted(QWidget *, QWidget *)'),
                        self, SIGNAL('unsetSend1()'))
        QObject.connect(self.send2Slot, SIGNAL('added(QWidget *, QWidget *)'),
                        self.setSend)
        QObject.connect(self.send1Slot,
                        SIGNAL('deleted(QWidget *, QWidget *)'),
                        self, SIGNAL('unsetSend2()'))

        Layout = QHBoxLayout(self)
        Layout.addWidget(self.label)
        Layout.addWidget(self.mapper)
#        Layout.addStretch(20)
        Layout.addWidget(self.send1Slot)
        Layout.addWidget(self.send2Slot)
        #pk.widgets.utils.h_centered(Layout, self.send1Slot)
        #pk.widgets.utils.h_centered(Layout, self.send2Slot)
#        ModeLayout = QGridLayout()
        ModeLayout = QHBoxLayout()
        Layout.addLayout(ModeLayout)
        for index, button in enumerate(self.modeButtons):
            #ModeLayout.addWidget(button, index % 2, index / 2)
            ModeLayout.addWidget(button)
            #pk.widgets.utils.h_centered(Layout, button)
        Layout.addStretch(1)
        #Layout.addWidget(self.clickButton)
        pk.widgets.utils.h_centered(Layout, self.clickButton)


    def setSend(self, part, slot):
        if slot == self.send1Slot:
            self.emit(SIGNAL('setSend1(QWidget *)'), part)
        if slot == self.send2Slot:
            self.emit(SIGNAL('setSend2(QWidget *)'), part)

    
if __name__ == '__main__':
    import pk.widgets.utils
    pk.widgets.utils.run_widget(ControlPanel)
