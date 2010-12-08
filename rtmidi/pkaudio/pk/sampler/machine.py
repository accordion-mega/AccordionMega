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
Global controls

this is purely organizational
"""

import os
from PyQt4.QtCore import QObject, SIGNAL, QTimer, Qt
from PyQt4.QtGui import *
import pk.widgets
from pk.widgets.utils import POV_COLOR
import midi
import sequencer


class QuitterLabel(QLabel):
    def mouseReleaseEvent(self, e):
        QApplication.instance().quit()


class MachineControl(QFrame):
    """ Controls global info. """

    def __init__(self, parent=None):
        QFrame.__init__(self)
        
        self.label = QuitterLabel('pksampler', self)
        self.label.setScaledContents(True)
        self.label.font().setPointSize(65)
        self.label.palette().setColor(QPalette.WindowText, QColor(60, 60, 80))

        self.modeGroup = QButtonGroup(self)
        self.modeGroup.setExclusive(True)
        self.buttons = []
        for mode in ('select', 'play', 'edit', 'delete'):
            button = pk.widgets.Button(self)
            button.setText(mode)
            button.setCheckable(True)
            setattr(self, mode+'Button', button)
            self.modeGroup.addButton(button)
            self.buttons.append(button)

        self.inputMapper = midi.InputWidget(self)
        self.inputMapper.font().setPointSize(15)
        self.inputMapper.setFixedWidth(110)

        self.metroButton = pk.widgets.Button(self, color='green')
        self.metroButton.setCheckable(True)
        self.metroButton.setText('metro')

        self.steady = pattern.Pattern([pattern.Note(0, 16, 60)])
        self.steady.beats = 1
        self.click = sequencer.Sample()

        ButtonLayout = QHBoxLayout()
        for button in self.buttons:
            ButtonLayout.addWidget(button)
        Layout = QHBoxLayout(self)
        Layout.addWidget(self.label)
        Layout.addStretch(1)
        Layout.addLayout(ButtonLayout)
        Layout.addStretch(1)
        Layout.addWidget(self.metroButton)
        Layout.addWidget(self.inputMapper)


if __name__ == '__main__':
    from pk.widgets.utils import run_widget
    run_widget(MachineControl)
