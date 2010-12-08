"""
A user-editable label.
"""


from PyQt4.QtCore import SIGNAL, QObject, Qt
from PyQt4.QtGui import QMouseEvent, QMatrix, QColor, QFont, QWidget, QLabel
from PyQt4.QtGui import QLineEdit, QPainter, QPalette


class Input(QLineEdit):
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        font = QFont('Trebuchet MS, Bold Italic')
        font.setPointSize(15)
        self.setFont(font)
        
    def focusOutEvent(self, e):
        self.hide()
        QLineEdit.focusOutEvent(self, e)

class TextLabel(QLabel):
    """ TODO: Make this editable, and vertical.
        SIGNALS:
            PYSIGNAL('textChanged'), (text,)
    """
    def __init__(self, text="TextLabel", parent=None):
        QLabel.__init__(self, text, parent)
        self.palette().setColor(QPalette.Window, QColor('white'))

        self.input = Input(self.parent())        
        self.input.hide()
        QObject.connect(self.input, SIGNAL('textChanged(const QString &)'),
                        self.setText)
        QObject.connect(self.input, SIGNAL('textChanged(const QString &)'),
                        self.slotTextChanged)
        QObject.connect(self.input, SIGNAL('returnPressed()'),
                        self.input.hide)

        font = QFont('Trebuchet MS, Bold Italic')
        font.setPointSize(10)
        self.setFont(font)
        self.setFixedSize(16, 95)
        self.edittable = False

    def setEdittable(self, on):
        self.edittable = on
                          
    def moveEvent(self, e):
        self.input.move(e.pos().x(), e.pos().y())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setPen(self.palette().color(QPalette.Text))
        m = QMatrix()
        m.rotate(-90)
        m.translate(-94, 2)
        p.setMatrix(m)
        p.drawText(3, 10, self.text())

    def isEditting(self):
        return self.input.isShown()

    def endEdit(self):
        self.input.hide()

    def edit(self):
        if self.edittable:
            self.input.setText(self.text())
            self.input.raise_()
            self.input.show()
            self.input.selectAll()
            self.input.setFocus()
        
    def mouseReleaseEvent(self, e):
        self.edit()
        
    def slotTextChanged(self, text):
        self.emit(SIGNAL('textChanged'), (text, ))

    def setText(self, text):
        self.input.setText(text)
        QLabel.setText(self, text)


if __name__ == '__main__':
    import utils
    utils.run_widget(TextLabel)
