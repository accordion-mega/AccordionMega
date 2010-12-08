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
Time-wise value bending
"""
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QWidget, QHBoxLayout, QPalette
import pk.widgets
import spec


class Bender(QObject):
    """ emits a bent version of its own value. """
    
    state = None
    interval = 10
    res = .1
    range = 8
    value = 0
    
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._timer = None
        self.bent = None
        
    def timerEvent(self, e):
        if self.state == 'up':
            self.bent += self.res
            if self.bent >= self.value + self.range:
                self._stop()
        elif self.state == 'down':
            self.bent -= self.res
            if self.bent <= self.value - self.range:
                self._stop()
        elif self.state == 'back':
            if self.bent > self.value:
                self.bent -= self.res
                if self.bent <= self.value:
                    self._stop()
            elif self.bent < self.value:
                self.bent += self.res
                if self.bent >= self.value:
                    self._stop()
        self.emit(SIGNAL('valueChanged(float)'), self.bent)
    
    def _stop(self):
        self.killTimer(self._timer)
        self.state = None

    def _start(self):
        if not self._timer is None:
            self.killTimer(self._timer)
        self._timer = self.startTimer(self.interval)

    def setValue(self, value):
        """ set the nominal value (to bend to/from) """
        self.value = float(value)
        if self.state is None:
            self.bent = self.value
        self.emit(SIGNAL('valueChanged(float)'), self.value)

    def bendUp(self):
        """ start bending up. """
        self.state = 'up'
        self.bent = self.value
        self._start()

    def bendDown(self):
        """ start bending down. """
        self.state = 'down'
        self.bent = self.value
        self._start()

    def bendBack(self):
        """ start bending back. """
        self.state = 'back'
        self._start()


class Buttons(QWidget):
    """ a throw away class """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(QPalette.Window, spec.POV_COLOR)

        self.upButton = pk.widgets.Button(self)
        self.upButton.setText('+')
        self.downButton = pk.widgets.Button(self)
        self.downButton.setText('-')

        Layout = QHBoxLayout(self)
        Layout.setSpacing(0)
        Layout.setMargin(0)
        Layout.addWidget(self.downButton)
        Layout.addWidget(self.upButton)

        QObject.connect(self.upButton, SIGNAL('pressed()'),
                        self, SIGNAL('bendUp()'))
        QObject.connect(self.downButton, SIGNAL('pressed()'),
                        self, SIGNAL('bendDown()'))
        QObject.connect(self.upButton, SIGNAL('released()'),
                        self, SIGNAL('bendBack()'))
        QObject.connect(self.downButton, SIGNAL('released()'),
                        self, SIGNAL('bendBack()'))


if __name__ == '__main__':
    import pk.widgets.utils
    class TestButtons(Buttons):
        def __init__(self):
            Buttons.__init__(self)
            self.bender = Bender(self)
            QObject.connect(self, SIGNAL('bendUp()'),
                            self.bender.bendUp)
            QObject.connect(self, SIGNAL('bendDown()'),
                            self.bender.bendDown)
            QObject.connect(self, SIGNAL('bendBack()'),
                            self.bender.bendBack)
            QObject.connect(self.bender, SIGNAL('valueChanged(float)'),
                            self.print_value)
        def print_value(self, value):
            print value
    pk.widgets.utils.run_widget(TestButtons)
