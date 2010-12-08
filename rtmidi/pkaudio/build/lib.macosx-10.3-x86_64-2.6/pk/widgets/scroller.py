"""
Magic scroll area preview scroller.
"""

from preview import WidgetPreview
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QWidget, QPainter, QColor


class PreviewScroller(WidgetPreview):
    """ A necessary preview scrollbar. """

    def __init__(self, scrollarea, parent=None):
        self.scrollarea = scrollarea
        widget = scrollarea.widget()
        if widget is None:
            raise ValueError('scrollarea has no widget')
        WidgetPreview.__init__(self, widget, parent=None)
        QObject.connect(widget, SIGNAL('destroyed()'), self.disconnectWidget)

        self.box_color = QColor('yellow')
        self._last_x = None
        self._last_y = None
        self.setMouseTracking(False)

    def disconnectWidget(self):
        self.widget = None
        self._last_x = None
        self._last_y = None

    def _factor(self):
        x_fact = float(self.width()) / float(self.widget.width())
        y_fact = float(self.height()) / float(self.widget.height())
        return x_fact, y_fact

    def _translate(self, rect):
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        x_fact, y_fact = self._factor()
        return (int(x * x_fact), int(y * y_fact),
                int(w * x_fact), int(h * y_fact))

    def paintEvent(self, e):
        """ draw the viewport box. """
        WidgetPreview.paintEvent(self, e)
        if self.widget:
            rect = self.widget.visibleRegion().boundingRect()
            x, y, w, h = self._translate(rect)
            painter = QPainter(self)
            pen = painter.pen()
            pen.setWidth(5)
            pen.setColor(self.box_color)
            painter.setPen(pen)
            painter.drawRect(x, y, w, h)
            painter.end()

    def mouseReleaseEvent(self, e):
        self._last_x = None
        self._last_y = None

    def mouseMoveEvent(self, e):
        if self._last_x != None and self._last_y != None:
            x_diff = e.x() - self._last_x
            y_diff = e.y() - self._last_y

            x_fact, y_fact = self._factor()
            x_diff *= 1 / x_fact
            y_diff *= 1 / y_fact

            h_bar = self.scrollarea.horizontalScrollBar()
            v_bar = self.scrollarea.verticalScrollBar()

            vx = h_bar.value() + x_diff
            h_bar.setValue(vx)
            vy = v_bar.value() + y_diff
            v_bar.setValue(vy)

        self._last_x = e.x()
        self._last_y = e.y()
        self.update()



if __name__ == '__main__':
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import QApplication, QSlider, QScrollArea
    from PyQt4.QtGui import QPushButton, QWidget, QVBoxLayout
    
    app = QApplication([])

    widget = QWidget()
    Layout = QVBoxLayout(widget)
    for i in range(10):
        button = QPushButton('button %i' % i, widget)
        Layout.addWidget(button)
    widget.setFixedSize(600, 800)
    widget.show()

    scrollarea = QScrollArea()
    scrollarea.setWidget(widget)
    scrollarea.resize(300, 300)
    scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scrollarea.show()

    scroller = PreviewScroller(scrollarea)
    scroller.resize(400, 400)
    scroller.show()
    
    app.exec_()

