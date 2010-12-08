"""
A widget preview.
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel, QPixmap


class WidgetPreview(QLabel):

    interval = 1000
    
    def __init__(self, widget, parent=None):
        QLabel.__init__(self, parent)
        self.widget = widget
        self.setScaledContents(True)
        self._timer = None
        
    def start_update(self, interval=None):
        if interval:
            self.interval = interval
        if not self._timer is None:
            self.killTimer(self._timer)
        self._timer = self.startTimer(self.interval)

    def update_preview(self):
        if self.widget:
            snapshot = QPixmap.grabWidget(self.widget)
            self.snapshot = snapshot
            self.setPixmap(self.snapshot)

    def timerEvent(self, e):
        """ take a snapshot """
        self.update_preview()


if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QSlider, QPalette, QColor, QScrollArea
    from PyQt4.QtGui import QPushButton, QWidget, QHBoxLayout
    
    app = QApplication([])

    wmain = QWidget()
    Layout = QHBoxLayout(wmain)
    
    slider = QWidget(wmain)
    palette = slider.palette()
    palette.setColor(QPalette.Window, QColor('green'))
    slider.setPalette(palette)
    slider.setFixedSize(640, 480)
    Layout.addWidget(slider)

    button = QPushButton('hey', wmain)
    palette = slider.palette()
    palette.setColor(QPalette.Window, QColor('red'))
    slider.setPalette(palette)
    slider.setFixedSize(600, 400)
    Layout.addWidget(button)
    
    #scroll = QScrollArea()
    #scroll.setWidget(wmain)
    #scroll.resize(200, 300)
    #scroll.show()

    wmain.show()
    #wmain.scroll(100, 100)
    print wmain.x(), wmain.y(), wmain.width(), wmain.height()
    
    preview = WidgetPreview(wmain)
    preview.resize(100, 100)
    preview.show()
    
    app.exec_()

