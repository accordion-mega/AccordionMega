""" Edit a rectangular box over a pixmap. """

from PyQt4.QtCore import QObject, SIGNAL, Qt, QRect
from PyQt4.QtGui import QWidget, QColor, QVBoxLayout, QPalette, QSizePolicy
from PyQt4.QtGui import QHBoxLayout, QSpinBox, QPainter

class BoxEditor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.palette().setColor(QPalette.Window, QColor('black'))
    
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.pressed = False
        self.pixmap = None
        self.color = QColor('red')
        
    def setLineColor(self, c):
        self.color = c
        
    # mask setters
    
    def sizeHint(self):
        if self.pixmap:
            return self.pixmap.size()
        else:
            return QWidget.sizeHint(self)
            
    def mousePressEvent(self, e):
        self.pressed = True
        self.x = e.x()
        self.y = e.y()
        QWidget.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e):
        """ for single clicks; keep from remving the box """
        QWidget.mouseReleaseEvent(self, e)
        
    def mouseMoveEvent(self, e):
        if self.pressed:
            self.w = e.x() - self.x
            self.h = e.y() - self.y
            self.setValue(self.x,self.y,self.w,self.h)
        QWidget.mouseMoveEvent(self, e)

    def paintEvent(self, e):
        QPainter(self).drawPixmap(self, 0, 0, self.pixmap)
        QWidget.paintEvent(self, e)
            
    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        if self.pixmap.isNull():
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            self.setFixedSize(self.pixmap.size())
        self.update()
        
    def setValue(self, x, y, w, h):
        self.setValue_noemit(x, y, w, h)
        self.emit(SIGNAL('valueChanged'), self.value())

    def setValue_noemit(self, x, y, w, h):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if w < 0:
            w = 0
        if h < 0:
            h = 0
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.update()        
        
    def value(self):
        """ Returns the mask defined by the window in a tuple. """
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        return (x,y,w,h)
        if self.w < 0:
            x = self.x + self.w
            w = abs(self.w)
        if self.h < 0:
            y = self.y + self.h
            h = abs(self.h)
        return (x, y, w, h)        

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(self.color)
        painter.setBrush(Qt.NoBrush)
        rect = QRect(self.x,self.y,self.w,self.h)
        painter.drawRect(rect)
        QWidget.paintEvent(self, e)


class MaskEditor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        Layout = QVBoxLayout(self)
        
        self.editor = BoxEditor(self)
        QObject.connect(self.editor, SIGNAL('valueChanged'),
                        self.slotBoxEditor)
        Layout.addWidget(self.editor)

        ControlLayout = QHBoxLayout()
        Layout.addLayout(ControlLayout)

        for i in ('x', 'y', 'w', 'h'):
            name = i+'SpinBox'
            s = QSpinBox(self)
            s.setMaximum(5000)
            s.setMinimum(-5000)
            QObject.connect(s, SIGNAL('valueChanged(int)'),
                            self.slotSpinBox)
            setattr(self, name, s)
            ControlLayout.addWidget(s)

    def slotSpinBox(self):
        x = self.xSpinBox.value()
        y = self.ySpinBox.value()
        w = self.wSpinBox.value()
        h = self.hSpinBox.value()
        self.editor.setValue_noemit(x,y,w,h)
        self.emit(SIGNAL('valueChanged'), (self.value(), ))

    def slotBoxEditor(self):
        x,y,w,h = self.editor.value()
        self.xSpinBox.setValue(x)
        self.ySpinBox.setValue(y)
        self.wSpinBox.setValue(w)
        self.hSpinBox.setValue(h)
        self.emit(SIGNAL('valueChanged'), (self.value(), ))
        
    def boxEditor(self):
        return self.editor

    def setPixmap(self, pixmap):
        self.editor.setPixmap(pixmap)

    def value(self):
        """ (x,y,w,h) """
        return self.editor.value()

    def setValue(self, x, y, w, h):
        self.editor.setValue(x, y, w, h)

