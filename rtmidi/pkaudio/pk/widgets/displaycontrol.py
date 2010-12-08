"""
A widget that has a little lcd display.
"""

from PyQt4.QtCore import Qt, QObject, SIGNAL, QRect
from PyQt4.QtGui import QColor, QPainter, QFont, QPalette, QPixmap, QWidget
from PyQt4.QtGui import QVBoxLayout, QLabel
from utils import h_centered


FONT = 'Andale Mono'
PIXMAP_PATH = ':/povray/display_background.png' 
COLOR = QColor(58, 58, 58)


class Display(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self._pixmap = QPixmap(PIXMAP_PATH)
        self.setFixedSize(self._pixmap.size())
        #font = QFont()
        #font.setFamily(FONT)
        #font.setPointSize(7)
        #self.setFont(font)
        palette = self.palette()
        palette.setColor(QPalette.Text, COLOR)
        self.setPalette(palette)
        self.setMargin(2)
        #self.setIndent(2)
        self.setAlignment(Qt.AlignHCenter)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap(PIXMAP_PATH))
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawText(rect, Qt.AlignCenter, self.text())
        painter.end()
        #return QLabel.paintEvent(self, e)


class DisplayControl(QWidget):
    """ Provides a qobject signal interface that's good for mapping. """
    def __init__(self, widget, parent=None):
        QWidget.__init__(self, parent)
        Layout = QVBoxLayout(self)
        Layout.setMargin(0)
        Layout.setSpacing(0)
        
        self.display = Display(self)
        h_centered(Layout, self.display)

        self.widget = widget
        self.widget.setParent(self)
        Layout.addWidget(self.widget)

        SIGNALS = ('clicked()', 'clicked(bool)',
                   'pressed()', 'released()',
                   'toggled(bool)', 'moved(int)')
        for sig in SIGNALS:
            QObject.connect(self.widget, SIGNAL(sig),
                            self, SIGNAL(sig))
        self.setFixedSize(widget.width(),
                          widget.height() + self.display.height())
        self.text = self.display.text
        self.setText = self.display.setText

    def clicked(self):
        self.emit(SIGNAL('clicked()'))

    def moved(self, value):
        self.emit(SIGNAL('moved(int)'), value)


if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    from pk.widgets.button import Button
    a = QApplication([])
    button = Button()
    display = DisplayWidget(button)
    display.show()
    a.exec_()
    
