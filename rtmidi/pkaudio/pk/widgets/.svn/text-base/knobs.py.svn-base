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
a nice scrunched collection of knobs
"""

import utils
import povwidgets
from PyQt4.QtGui import QWidget, QPalette


class Knobs(QWidget):
    """ scrunches knobs down tight. """
    def __init__(self, knobs=10, parent=None):
        QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(QPalette.Window, utils.POV_COLOR)
        
        self.knobs = [povwidgets.Knob(self) for i in range(knobs)]
        y = 0
        width = 0
        height = 0
        for index, knob in enumerate(self.knobs):
            if index % 2:
                x = 0
            else:
                x = (knob.width() / 3) * 2
            knob.move(x, y)
            y += knob.height() - 15
            height = knob.y() + knob.height()
            if x + knob.width() > width:
                width = x + knob.width()
        self.setFixedSize(width, height)


if __name__ == '__main__':
    import utils
    utils.run_widget(Knobs)
