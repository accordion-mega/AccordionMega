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

from PyQt4.QtCore import Qt, QObject, SIGNAL
from PyQt4.QtGui import QScrollArea, QFrame, QHBoxLayout, QVBoxLayout, QColor
import scrollbar


class ScrollArea(QFrame):

    def __init__(self, parent=None, horizontal=True, vertical=True,
                 color=None):
        QFrame.__init__(self, parent)
        
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.v_pad = scrollbar.ScrollPad(self)
        self.v_pad.setOrientation(Qt.Vertical)
        self.v_pad.setMinimumWidth(30)
        if color:
            self.v_pad.set_color(color)

        self.h_pad = scrollbar.ScrollPad(self)
        self.h_pad.setOrientation(Qt.Horizontal)
        self.h_pad.setMinimumHeight(30)
        if color:
            self.h_pad.set_color(color)

        QObject.connect(self.v_pad, SIGNAL('valueChanged(int)'),
                        self.v_scroll)
        QObject.connect(self.h_pad, SIGNAL('valueChanged(int)'),
                        self.h_scroll)

        for name in ('setWidgetResizable',):
            setattr(self, name, getattr(self.scrollarea, name))
        self.horizontal(horizontal)
        self.vertical(vertical)

        Layout1 = QVBoxLayout(self)
        Layout1.setSpacing(0)
        Layout1.setMargin(0)
        Layout2 = QHBoxLayout()
        Layout2.setSpacing(0)
        Layout2.setMargin(0)
        Layout2.addWidget(self.scrollarea)
        Layout2.addWidget(self.v_pad)
        Layout1.addLayout(Layout2)
        Layout1.addWidget(self.h_pad)

    def setWidget(self, widget):
        self.scrollarea.setWidget(widget)

    def horizontal(self, on):
        if on:
            self.h_pad.show()
        else:
            self.h_pad.hide()

    def vertical(self, on):
        if on:
            self.v_pad.show()
        else:
            self.v_pad.hide()

    def v_scroll(self, value):
        sb = self.v_pad
        target_sb = self.scrollarea.verticalScrollBar()
        percent = sb.value() / float(sb.maximum())
        target_sb.setValue(int(percent * target_sb.maximum()))

    def h_scroll(self, value):
        sb = self.h_pad
        target_sb = self.scrollarea.horizontalScrollBar()
        percent = sb.value() / float(sb.maximum())
        target_sb.setValue(int(percent * target_sb.maximum()))


if __name__ == '__main__':
    from pk.widgets.utils import run_widget
    from PyQt4.QtGui import QLabel, QPixmap
    class TestScrollArea(ScrollArea):
        def __init__(self, parent=None):
            ScrollArea.__init__(self, parent)
            widget = QLabel()
            widget.setPixmap(QPixmap(':/static/pkstudio_bg.png'))
            widget.setFixedSize(1000, 1000)
            self.setWidget(widget)

    run_widget(TestScrollArea)

