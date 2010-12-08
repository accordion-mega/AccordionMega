"""
A common base class for all pk widgets.
"""

from PyQt4.QtGui import QFrame, QPalette, QPainter, QColor

class PKWidget(QFrame):
    """ Conveinience class """
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        palette = self.palette()
        self._backgroundColor = palette.color(self.backgroundRole())
    
    def set_background(self, color):
        self._backgroundColor = color
        #palette = QPalette()
        #palette.setColor(self.backgroundRole(), color)
        #self.setPalette(palette)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QColor(self._backgroundColor))
        painter.setBrush(QColor(self._backgroundColor))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.end()
        QFrame.paintEvent(self, e)

