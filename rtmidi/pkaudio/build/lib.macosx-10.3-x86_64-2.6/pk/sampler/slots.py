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
from PyQt4.QtGui import QFrame, QPainter, QColor, QBrush
import spec


class PartSlot(QFrame):
    """ Volume, knobs. """

    margin = 3
    partname = None
    action = Qt.CopyAction
    active = True
    part = None
    frame_color = QColor('red').dark(150)
    
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAcceptDrops(True)
        self.setFixedWidth(spec.PART_WIDTH + self.margin * 2)
        self.setFixedHeight(spec.PART_HEIGHT + self.margin * 2)

    def dragEnterEvent(self, e):
        if self.partname is None or e.mimeData().text() == self.partname:
            e.acceptProposedAction()

    def dropEvent(self, e):
        if e.proposedAction() == self.action:
            e.acceptProposedAction()
            part = e.mimeData().part
            if hasattr(part.parent(), 'remove'):
               part.parent().remove(part)
            self.add(part)

    def paintEvent(self, e):
        if self.active:
            painter = QPainter(self)
            pen = painter.pen()
            pen.setWidth(self.margin)
            pen.setColor(self.frame_color)
            color = QColor(self.frame_color)
            color.setAlpha(30)
            painter.setBrush(color)
            painter.drawRect(0, 0, self.width(), self.height())

    def add(self, part):
        part.setParent(self)
        part.show()
        part.move(self.margin, self.margin)
        QObject.connect(part, SIGNAL('selected(QWidget *)'),
                        self, SIGNAL('selected(QWidget *)'))
        self.part = part
        self.emit(SIGNAL('added(QWidget *, QWidget *)'), part, self)
        return self.part

    def remove(self, part):
        if self.part:
            self.part.setParent(None)
            part = self.part
            self.part = None
            self.emit(SIGNAL('deleted(QWidget *, QWidget *)'), part, self)
            return part


class SynthSlot(PartSlot):

    partname = 'LoopPart'

    def __init__(self, parent=None):
        PartSlot.__init__(self, parent)

    def add(self, part):
        newpart = PartSlot.add(self, part)
        if not part.pattern is None:
            newpart.pattern = part.pattern
        newpart.activeLED.show()
        newpart.setAcceptDrops(True)
        
    def remove(self, part):
        part = PartSlot.remove(self, part)
        if part:
            part.setAcceptDrops(True)
            part.activeLED.hide()


class EffectSlot(PartSlot):

    partname = 'EffectPart'

    def __init__(self, parent=None):
        PartSlot.__init__(self, parent)

    def add(self, part):
        # do the routing
        part = PartSlot.add(self, part)
    
    def delete(self):
        # undo the routing
        PartSlot.delete(self)
    

if __name__ == '__main__':
    from PyQt4.QtGui import QWidget, QVBoxLayout
    import pk.widgets.utils
    import parts, synths
    class TestSlots(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)
            Layout = QVBoxLayout(self)
            self.slot = PartSlot(self)
            self.synth = SynthSlot(self)
            self.effect = EffectSlot(self)
            QObject.connect(self.slot, SIGNAL('selected(QWidget *)'),
                            self.slot.remove)
            QObject.connect(self.synth, SIGNAL('selected(QWidget *)'),
                            self.synth.remove)
            QObject.connect(self.effect, SIGNAL('selected(QWidget *)'),
                            self.effect.remove)
            Layout.addWidget(self.slot)
            Layout.addWidget(self.synth)
            Layout.addWidget(self.effect)

            self._part1 = parts.LoopPart(synths.Synth(), None)
            self._part2 = parts.EffectPart(synths.Synth(), None)
            self._part1.show()
            self._part2.show()
    pk.widgets.utils.run_widget(TestSlots)
