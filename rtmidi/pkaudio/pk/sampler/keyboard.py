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
from PyQt4.QtCore import *
from PyQt4.QtGui import *


WHITE_FILL = QColor(240, 240, 240)
WHITE_HILITE = QColor(255, 255, 255)
BLACK_FILL = QColor(0, 0, 0)
BLACK_HILITE = QColor(150, 150, 150)
PRESSED = QColor(200, 200, 100, 150)
KEY_ORDER = (0,1,0,1,0,0,1,0,1,0,1,0)


class Key(QWidget):

    note = None
    
    def __init__(self, parent, color, note, orientation):
        QWidget.__init__(self, parent)
        self.orientation = orientation
        self.note = note
        self.color = color
        if color == 'white':
            self.fill_color = WHITE_FILL
            self.hilite_color = WHITE_HILITE
        else:
            self.fill_color = BLACK_FILL
            self.hilite_color = BLACK_HILITE
        self.pressed_color = PRESSED
        self.pressed = False
        
    def paintEvent(self, e):
        painter = QPainter(self)
        # outline, fill
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(self.fill_color)
        painter.drawRect(0, 0, self.width() - 2, self.height() - 2)
        # hitlite
        painter.setPen(self.hilite_color)
        painter.setBrush(self.hilite_color)
        painter.drawRect(2, 1, self.width() / 10, self.height() - 4)
        if self.pressed:
            painter.setPen(self.pressed_color)
            painter.setBrush(self.pressed_color)
            painter.drawRect(1, 1, self.width() - 2, self.height() - 2)

    def vel(self, e):
        if self.orientation == Qt.Vertical:
            return (e.y() / float(self.height())) * 127
        else:
            return (e.x() / float(self.width())) * 127

    def mousePressEvent(self, e):
        self.pressed = True
        self.emit(SIGNAL('pressed(int, int)'), self.note, self.vel(e))
        QWidget.mousePressEvent(self, e)
        self.update()

    def mouseReleaseEvent(self, e):
        self.pressed = False
        self.emit(SIGNAL('released(int, int)'), self.note, self.vel(e))
        QWidget.mouseReleaseEvent(self, e)
        self.update()

    def mouseMoveEvent(self, e):
        QWidget.mouseMoveEvent(self, e)


class Keyboard(QWidget):

    halfsteps = 12 * 12 # ain't getting more than that!
    keywidth = 19
    
    def __init__(self, parent=None, orientation=Qt.Horizontal):
        QWidget.__init__(self, parent)
        Layout = QHBoxLayout(self)
        self.keys = []
        self.pressed_keys = []
        self.orientation = orientation
        
        self._createKeys()
        self._arrangeKeys()

    def _createKeys(self):
        # add new keys
        if len(self.keys) < self.halfsteps:
            key_index = 0
            last_white = None
            for i in range(self.halfsteps / 12):
                for ji, j in enumerate(KEY_ORDER):
                    if j:
                        key = Key(self, 'black', None, self.orientation)
                        key.white_parent = last_white
                    else:
                        key = Key(self, 'white', None, self.orientation)
                        last_white = key
                    key.note = i * 12 + ji
                    QObject.connect(key, SIGNAL('pressed(int, int)'),
                                    self.note_on)
                    QObject.connect(key, SIGNAL('released(int, int)'),
                                    self.note_off)
                    key.index = key_index
                    self.keys.append(key)
                    
        # hide extras
        for index, key in enumerate(self.keys):
            if index + 1 > self.halfsteps:
                key.hide()
            else:
                key.show()

    def _arrangeKeys(self):
        off = 0
        for index, key in enumerate(self.keys):
            if not key.isHidden():
                if self.orientation == Qt.Horizontal:
                    key.resize(self.keywidth, self.height())
                    key.move(off, 0)
                else:
                    key.move(0, off)
                    key.resize(self.width(), self.keywidth)
            off += self.keywidth

    def resizeEvent(self, e):
        self._arrangeKeys()

    def setHalfSteps(self, n):
        self.halfsteps = n
        self._arrangeKeys()

    def setOrientation(self, orientation):
        self.orientation = orientation
        for key in self.keys:
            key.orientation = orientation
        self.update()
        
    def pressedKeys(self):
        return [key for key in self.keys if key.pressed]

    def note_on(self, note, vel):
        if self.orientation == Qt.Vertical:
            note = self.halfsteps - note
        self.emit(SIGNAL('noteon(int, int)'), note, vel)

    def note_off(self, note, vel):
        if self.orientation == Qt.Vertical:
            note = self.halfsteps - note
        self.emit(SIGNAL('noteoff(int, int)'), note, vel)


if __name__ == '__main__':
    def noteon(note, vel):
        print 'NOTE-ON', note, vel
    def noteoff(note, vel):
        print 'NOTE-OFF', note, vel

    a = QApplication([])
    
    k1 = Keyboard(orientation=Qt.Horizontal)
    k1.setHalfSteps(4 * 12)
    k1.resize(190 * 4, 80)
    k1.show()
    
    k2 = Keyboard(orientation=Qt.Vertical)
    k2.setHalfSteps(3 * 12)
    k2.resize(80, 190 * 3)
    k2.show()

    QObject.connect(k1, SIGNAL('noteon(int, int)'), noteon)
    QObject.connect(k1, SIGNAL('noteoff(int, int)'), noteoff)    
    QObject.connect(k2, SIGNAL('noteon(int, int)'), noteon)
    QObject.connect(k2, SIGNAL('noteoff(int, int)'), noteoff)    
    k1.move(k2.x() + 100, k1.y())
    a.exec_()
