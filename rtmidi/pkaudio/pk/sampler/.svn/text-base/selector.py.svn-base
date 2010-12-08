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
Draggable items selector.
"""

from PyQt4.QtCore import QEvent
from PyQt4.QtGui import QFrame
import spec


class Selector(QFrame):

    margin = 2
    
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setFixedWidth(spec.PART_WIDTH + self.margin * 2)
        self.parts = []

    def add(self, part):
        part.setParent(self)
        part.show()
        self.parts.append(part)
        self._rearrange()

    def remove(self, part):
        self.parts.remove(part)
        self._rearrange()

    def _sort(self):
        pass

    def _rearrange(self):
        """ also cleanup adopted children """
        self._sort()
        y = 0
        for part in self.parts:
            part.move(self.margin, y)
            y += part.height()
        if self.width() > -1:
            self.setFixedSize(self.width(), y)
        else:
            self.setFixedHeight(y)

    def childEvent(self, e):
        if e.type() == QEvent.ChildRemoved:
            self._rearrange()


if __name__ == '__main__':
    from pk.widgets.utils import run_widget
    import parts
    import synths
    class TestSelector(Selector):
        def __init__(self):
            Selector.__init__(self)

            for i in range(5):
                self.add(parts.SynthPart(synths.Sine()))
                self.add(parts.SynthPart(synths.Sample()))
    run_widget(TestSelector)

