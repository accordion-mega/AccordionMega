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
X-Y goodness
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QColor, QPainter


class Graph(QWidget):
    """ Remember algebra? I don't. """
    
    x = None
    y = None

    line_brush = QColor('yellow')
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMouseTracking(False)

    def resizeEvent(self, e):
        if self.x is None:
            self.x = self.width() / 2
        if self.y is None:
            self.y = self.height() / 2
        
    def mouseMoveEvent(self, e):
        self.x = e.x()
        self.y = e.y()
        self.update()
        self.emit(SIGNAL('valueChanged(int, int)'), (self.x, self.y))
        
    def paintEvent(self, e):
        painter = QPainter(self)

        painter.setPen(QColor('black'))
        painter.setBrush(QColor('black'))
        painter.drawRect(0, 0, self.width(), self.height())
        
        painter.setPen(self.line_brush)
        painter.setBrush(self.line_brush.dark(150))
        painter.drawLine(self.x, 0, self.x, self.height())
        painter.drawLine(0, self.y, self.width(), self.y)



if __name__ == '__main__':
    from pk.widgets import utils
    utils.run_widget(Graph)
