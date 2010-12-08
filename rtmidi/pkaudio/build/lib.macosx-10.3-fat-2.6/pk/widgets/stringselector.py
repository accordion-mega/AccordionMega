"""
Generic string selector.
"""

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QPushButton, QApplication, QWidget, QVBoxLayout, QFont
from PyQt4.QtGui import QButtonGroup, QPalette, QColor, QLabel, QHBoxLayout, QVBoxLayout
from pk.widgets import Button


class Option(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Layout = QHBoxLayout(self)
        Layout.setMargin(0)
        
        self.button = Button(self)
        palette = QPalette(self.button.palette())
        palette.setColor(QPalette.Button, QColor('grey').dark(150))
        self.button.setPalette(palette)
        QObject.connect(self.button, SIGNAL('clicked()'), self.clicked)
        Layout.addWidget(self.button)
        
        self.label = QLabel(self)
        self.label.setFrameShape(QLabel.Panel)
        self.label.setFixedHeight(self.button.height())
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        palette = QPalette(self.label.palette())
        palette.setColor(QPalette.Window, QColor(151, 169, 0))
        self.label.setPalette(palette)
        Layout.addWidget(self.label)

    def clicked(self):
        self.emit(SIGNAL('selected(QString &)'), self.label.text())


class Selector(QWidget):
    def __init__(self, parent=None, orientation=Qt.Vertical):
        QWidget.__init__(self, parent)
        if orientation == Qt.Vertical:
            Layout = QVBoxLayout(self)
        else:
            Layout = QHBoxLayout(self)
        Layout.setMargin(0)
        Layout.setSpacing(2)
        self.options = []

    def setOptions(self, options, text='select'):
        options = [str(i) for i in options]
        for widget in self.options:
            widget.hide()
        for index, value in enumerate(options):
            if index < len(self.options):
                option = self.options[index]
            else:
                option = Option(self)
                QObject.connect(option, SIGNAL('selected(QString &)'),
                                self, SIGNAL('selected(QString &)'))
                self.layout().addWidget(option)
                self.options.append(option)
            option.show()
            option.label.setText(value)
            option.button.setText(text)


def main():
    import sys
    import random
    def selected(value):
        global w
        print 'Selected:',value
        options = [random.randint(0, 1000) for i in range(random.randint(5,7))]
        w.setOptions(options, str(random.randint(0, 10000)))
    a = QApplication(sys.argv)
    w = Selector()
    w.resize(300, 300)
    w.setOptions(('hey', 'you', 'guys,', 'uh', 'huh'))
    palette = w.palette()
    palette.setColor(QPalette.Window, QColor(136, 136, 136))
    w.setPalette(palette)
    QObject.connect(w, SIGNAL('selected(QString &)'), selected)
    w.show()
    a.exec_()



if __name__ == '__main__':
    main()
