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
Beat Matching equipment.
"""

from PyQt4.QtCore import SIGNAL, Qt, QObject, QTimer, QPointF, QRectF
from PyQt4.QtGui import QWidget, QColor, QPainter, QVBoxLayout, QLabel
from PyQt4.QtGui import QPalette, QFrame, QHBoxLayout, QFontMetrics
import pk.widgets
import bender
import spec


class History(QFrame):
    """ Tracers! I see Tracers! """

    interval = 100
    q_len = 10
    upper = 170.0
    lower = 110.0
    background = QColor('black')
    bent_base = QColor(150, 0, 200, 200)
    nominal_base = QColor(0, 200, 200, 200)
    
    def __init__(self, bender, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.bender = bender
        self.nominal = []
        self.bent = []
        self.startTimer(self.interval)

    def timerEvent(self, e):
        if len(self.nominal) > self.q_len:
            self.nominal.remove(self.nominal[0])
        if len(self.bent) > self.q_len:
            self.bent.remove(self.bent[0])
        self.nominal.append(self.bender.value)
        self.bent.append(self.bender.bent)
        range = self.bender.range * 2.5
        self.upper = self.bender.value + range / 2.0
        self.lower = self.bender.value - range / 2.0
        self.update()

    def y_for(self, tempo):
        ratio = (tempo - self.lower) / (self.upper - self.lower)
        return self.height() - (ratio * self.height())

    def drawTempos(self, painter, tempos):
        inc = self.width() / self.q_len
        points = []
        for index, tempo in enumerate(tempos):
            x = inc * index
            y = self.y_for(tempo)
            points.append(QPointF(x, y))
        if points:
            painter.drawPolyline(*tuple(points))

    def drawTempo(self, painter, value):
        metric = QFontMetrics(painter.font())
        rect = metric.boundingRect(str(value))
        if rect.y() < 0:
            rect.adjust(0, abs(rect.y()), 0, 10)
        painter.drawText(rect, 0, str(value))

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.background)
        painter.setBrush(self.background)
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setPen(QColor(255, 255, 255, 200))
        self.drawTempo(painter, self.bender.bent)

        painter.setPen(self.nominal_base)
        painter.setBrush(self.nominal_base.light(200))
        painter.pen().setWidth(4)
        self.drawTempos(painter, self.nominal)
        painter.setPen(self.bent_base)
        painter.setBrush(self.bent_base.light(200))
        painter.pen().setWidth(2)
        self.drawTempos(painter, self.bent)


class Adjuster(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(self.backgroundRole(), spec.POV_COLOR)

        self.benderButtons = bender.Buttons(self)
        self.bender = bender.Bender(self)
        self.bender.setValue(150)
        self.wheelPad = pk.widgets.WheelPad(self)
        self.history = History(self.bender, parent=self)
        self.history.setMinimumHeight(50)
        
        QObject.connect(self.benderButtons, SIGNAL('bendUp()'),
                        self.bender.bendUp)
        QObject.connect(self.benderButtons, SIGNAL('bendDown()'),
                        self.bender.bendDown)
        QObject.connect(self.benderButtons, SIGNAL('bendBack()'),
                        self.bender.bendBack)
        QObject.connect(self.bender, SIGNAL('valueChanged(float)'),
                        self.emitTempo)
        QObject.connect(self.wheelPad, SIGNAL('moved_y(int)'),
                        self.slotWheel)
        
        Layout = QVBoxLayout(self)
        Layout.setMargin(0)
        Layout.addWidget(self.history)
        Layout.addWidget(self.benderButtons)
        Layout.setStretchFactor(self.benderButtons, 0)
        Layout.addWidget(self.wheelPad)
        Layout.setStretchFactor(self.wheelPad, 1)

    def slotWheel(self, delta):
        delta *= -.005
        self.bender.setValue(self.bender.value + delta)

    def emitTempo(self, tempo):
        self.emit(SIGNAL('valueChanged(float)'), tempo)


if __name__ == '__main__':
    import pk.widgets.utils
    import sys
    class Test(Adjuster):
        def __init__(self):
            Adjuster.__init__(self)
            QObject.connect(self, SIGNAL('valueChanged(float)'),
                            self.print_tempo)
#            self.history = History(self.bender)
#            self.history.show()
        def print_tempo(self, value):
            return
            print value
    pk.widgets.utils.run_widget(Test)
