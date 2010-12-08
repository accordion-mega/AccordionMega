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
A flashing light
"""

from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QFrame, QPainter, QColor


class LED(QFrame):

    color = QColor(255, 0, 0, 200)
    
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameShape(QFrame.Panel)
        self._on = False

    def paintEvent(self, e):
        if self._on:
            painter = QPainter(self)
            painter.setPen(self.color)
            painter.setBrush(self.color)
            painter.drawRect(0, 0, self.width(), self.height())
            
            painter.setPen(self.color.light(130))
            painter.setBrush(self.color.light(175))
            x_border = self.width() * .2
            y_border = self.height() * .2
            painter.drawEllipse(x_border, y_border,
                                self.width() - x_border * 2,
                                self.height() - y_border * 2)
            painter = None
        QFrame.paintEvent(self, e)

    def on(self):
        self._on = True
        self.update()

    def off(self):
        self._on = False
        self.update()

    def blink(self):
        self.on()
        QTimer.singleShot(300, self.off)

    def flashing(self):
        self.on()
        self._flashing = True
        self.keep_flashing()

    def stop(self):
        self._flashing = False

    def keep_flashing(self):
        if self._flashing:
            self.on()
            QTimer.singleShot(250, self.off)
            QTimer.singleShot(500, self.keep_flashing)


if __name__ == '__main__':
    from pk.widgets.utils import run_widget
    class TestLED(LED):
        def __init__(self):
            LED.__init__(self)
            self.flashing()
    run_widget(TestLED)
