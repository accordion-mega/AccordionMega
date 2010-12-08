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
touchscreen scrollers
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ScrollPad(QAbstractSlider):
    
    color = QColor('green')
    
    def __init__(self, parent=None):
        QAbstractSlider.__init__(self, parent)
        self.setMouseTracking(False)
        self._value = 0.0

    def setValue(self, value):
        self._value = float(value)
        QAbstractSlider.setValue(self, value)

    def set_color(self, color):
        self.color = color
        self.update()

    def mousePressEvent(self, e):
        self._last_x = e.x()
        self._last_y = e.y()

    def mouseMoveEvent(self, e):
        if self.orientation() == Qt.Vertical:
            diff = e.y() - self._last_y
        else:
            diff = e.x() - self._last_x
        diff /= 8.0
        self._last_x = e.x()
        self._last_y = e.y()
        
        self._value += diff
        if self._value > self.maximum():
            self._value = float(self.maximum())
        elif self._value < self.minimum():
            self._value = float(self.minimum())
        self.setValue(self._value)
        self.update()
        self.emit(SIGNAL('valueChanged(int)'), self.value())

    def mouseReleaseEvent(self, e):
        self._last_y = None

    def paintEvent(self, e):
        painter = QPainter(self)
        percent = self.value() / float(self.maximum())
        if percent == 1:
            percent = .9999
        elif percent == 0:
            percent = .0001
        low = percent - .1
        mid = percent
        high = percent + .1

        if low < 0:
            low = 0.0
        if high > 1:
            high = 1.0

        base = QColor(self.color)
        base.setAlpha(150)
        if self.orientation() == Qt.Vertical:
            gradient = QLinearGradient(0, 0, 0, self.height())
        else:
            gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(low, base.dark(200))
        gradient.setColorAt(mid, base)
        gradient.setColorAt(high, base.dark(200))
        painter.setBrush(QBrush(gradient))
        painter.drawRect(0, 0, self.width(), self.height())
        

class ScrollBar(QAbstractSlider):

    box_height = 40

    def __init__(self, parent=None):
        QAbstractSlider.__init__(self, parent)
        self.setFixedWidth(50)
        self.setTracking(True)
        self._last_y = 0
        
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().color(QPalette.Dark))

        y = self.value() - (self.box_height / 2)
        if y < 0:
            y = 0
        elif y > self.height() - self.box_height:
            y = self.height() - self.box_height
        painter.drawRect(0, y, self.width(), self.box_height)

    def resizeEvent(self, e):
        self.setMaximum(self.height())

    def mousePressEvent(self, e):
        self._last_y = 0
        self.setSliderDown(True)

    def mouseReleaseEvent(self, e):
        self.setSliderDown(False)

    def over_handle(self, e):
        y = self.value() - (self.box_height / 2)
        if y < 0:
            y = 0
        elif y > self.height() - self.box_height:
            y = self.height() - self.box_height
        return e.y() >= y or e.y() <= y + self.box_height

    def mouseMoveEvent(self, e):
        v = (e.y() - self.box_height / 2.0) / (self.height() - self.box_height) * self.maximum()
        self.setValue(v)
        self.update()
        self.emit(SIGNAL('valueChanged(int)'), self.value())



if __name__ == '__main__':
    app = QApplication([])

    parent = QWidget()
    parent.show()
    parent.resize(300, 300)
    Layout = QVBoxLayout(parent)
    HLayout = QHBoxLayout()
    Layout.addLayout(HLayout)

    w = QLabel()
    pixmap = QPixmap('/Users/patrick/repos.tulkas/pixmaps/icons/clover.png')
    w.setPixmap(pixmap)
    w.setScaledContents(True)
    w.resize(600, 600)

    scrollarea = QScrollArea(parent)
    scrollarea.setWidget(w)
    HLayout.addWidget(scrollarea)

    v_scrollpad = ScrollPad(parent)
    v_scrollpad.setOrientation(Qt.Vertical)
    v_scrollpad.setMinimumWidth(100)
    v_scrollpad.set_color(QColor('blue'))
    HLayout.addWidget(v_scrollpad)

    h_scrollpad = ScrollPad(parent)
    h_scrollpad.setOrientation(Qt.Horizontal)
    h_scrollpad.setMinimumHeight(75)
    h_scrollpad.set_color(QColor('red'))
    Layout.addWidget(h_scrollpad)

    def v_scroll(value):
        percent = value / float(v_scrollpad.maximum())
        sb = scrollarea.verticalScrollBar()
        sb.setValue(sb.maximum() * percent)
    def h_scroll(value):
        percent = value / float(h_scrollpad.maximum())
        sb = scrollarea.horizontalScrollBar()
        sb.setValue(sb.maximum() * percent)
        
    QObject.connect(v_scrollpad, SIGNAL('valueChanged(int)'), v_scroll)
    QObject.connect(h_scrollpad, SIGNAL('valueChanged(int)'), h_scroll)
    app.exec_()
    
