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
while-like adjuster pad
"""

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QWidget, QPainter, QColor


class WheelPad(QWidget):
    
    threshhold = 6
    accel_brush = QColor('red')
    diff_brush = QColor('blue')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._last_y = None
        self._last_x = None
        self._diff = None
    
    def paintEvent(self, e):
        painter = QPainter(self)
        if self._diff is None:
            color = QColor(self.diff_brush)
            color.setAlpha(25)
        else:
            color = self.diff_brush
            a = abs(self._diff) * 1.7
            if a > 75: a == 75
            color.setAlpha(25 + a)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(e.rect())

    def mousePressEvent(self, e):
        self._last_x = e.x()
        self._last_y = e.y()

    def mouseMoveEvent(self, e):
        x_diff = 0
        y_diff = 0
        if e.x() != self._last_x:
            x_diff = e.x() - self._last_x
            x_diff *= 4
            self._last_x = e.x()
            self.emit(SIGNAL('moved_x(int)'), x_diff)
        if e.y() != self._last_y:
            y_diff = e.y() - self._last_y
            self._last_y = e.y()
            self.emit(SIGNAL('moved_y(int)'), y_diff)
        self._diff = x_diff + y_diff / 2
        self.update()

    def mouseReleaseEvent(self, e):
        self._last_y = None
        self._last_x = None
        self._diff = None
        self.update()
        self.emit(SIGNAL('released()'))


if __name__ == '__main__':
    import utils
    class TestWheelPad(WheelPad):
        def __init__(self):
            WheelPad.__init__(self)
            QObject.connect(self, SIGNAL('moved_y(int)'),
                            self.print_value)
            QObject.connect(self, SIGNAL('moved_x(int)'),
                            self.print_value)
            QObject.connect(self, SIGNAL('released()'),
                            self.print_value)
        def print_value(self, value=None):
            print value
    utils.run_widget(TestWheelPad)
