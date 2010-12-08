"""
"""

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QButtonGroup, QWidget, QPushButton, QColor, QHBoxLayout, QPalette

ORDERED = (("Christmas", QColor('red').light(140)),
           ("Classical", QColor(255,255,0)),
           ("Blues", QColor('blue').light(140)),
           ("Jazz", QColor(0,255,0).light(140)),
           ("Folk", QColor(100, 100, 100).light(160)),
           ("Pop", QColor(255,186,243).light(140)),
           ("Rock", QColor(255,0,255).light(140)),
           ("Country", QColor(255, 170, 0).light(140)),
           ("Misc", QColor(100, 100, 100)),
           )

CATEGORIES = dict(ORDERED)

class CategoryButtons(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Layout = QHBoxLayout(self)
        self.group = QButtonGroup(self)
        for i, (k, color) in enumerate(ORDERED):
            button = QPushButton(k)
            palette = QPalette(button.palette())
            palette.setColor(QPalette.Button, color)
            button.setPalette(palette)
            self.group.addButton(button)
            self.group.setId(button, i)
            Layout.addWidget(button)
        QObject.connect(self.group,
                        SIGNAL('buttonClicked(QAbstractButton *)'),
                        self.clicked)

    def clicked(self, button):
        category = ORDERED[self.group.id(button)][0]
        self.emit(SIGNAL('selected(QString &)'), category)
    
