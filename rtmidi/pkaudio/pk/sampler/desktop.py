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
A Desktop
"""

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QLabel, QPainter, QColor, QPalette, QGridLayout, QPixmap


class Desktop(QLabel):
    """ gnerally statically-sized window. """
    
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(QPalette.Window, QColor('black'))
        self.setPixmap(QPixmap(':/static/pkstudio_bg.png'))
        self.components = []

    def add(self, component):
        """ good algorithms make good apps, shame i don't write algorithms. """
        component.setParent(self)
        x, y = 0, 0
        if self.components:
            comp = self.components[-1]
            x = comp.x() + comp.width()
            y = comp.y()
            # new column?
            if x + component.width() > self.width():
                x = 0
                last_row = [c for c in self.components if c.y() == comp.y()]
                
                # new row?
                for comp in last_row:
                    if comp.y() + comp.height() > y:
                        y = comp.y() + comp.height()
        component.move(x, y)
        component.show()
        self.components.append(component)

    def remove(self, component):
        component.setParent(None)

    def paintEvent(self, e):
        painter = QPainter(self)
        pixmap = self.pixmap()
        if pixmap:
            painter.drawTiledPixmap(0, 0, self.width(), self.height(), pixmap)

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication, QWidget

    class Component(QWidget):
        def __init__(self, color, size):
            QWidget.__init__(self)
            self.setAutoFillBackground(True)
            self.palette().setColor(QPalette.Window, QColor(color))
            self.resize(*size)
            self.color = color
    a = QApplication(sys.argv)
    desktop = Desktop()
    desktop.resize(640, 480)
    components = (Component('green', (200, 150)),
                  Component('red', (300, 40)),
                  Component('blue', (150, 100)),
                  Component('yellow', (300, 40)),
                  Component('maroon', (150, 100)),
                  Component('magenta', (150, 40)),
                  )
    for comp in components:
        desktop.add(comp)
    desktop.show()

    a.exec_()
