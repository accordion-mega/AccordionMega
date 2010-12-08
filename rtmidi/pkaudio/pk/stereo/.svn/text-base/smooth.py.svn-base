"""
Functions for making GUI transitions smooth.
"""

from PyQt4.QtCore import SIGNAL, QTimer, QObject
from PyQt4.QtGui import QWidget


ACTIONS = ('grow',
           'slide',
           )


def coord_path((x1, y1), (x2, y2), n):
    """ return a coordinate path between two points at a given resolution. """
    w1 = float(x1)
    w2 = float(x2)
    wd = (w2 - w1) / n

    h1 = float(y1)
    h2 = float(y2)
    hd = (h2 - h1) / n

    def it():
        for i in range(n):
            w = int(w1 + (i + 1) * wd)
            h = int(h1 + (i + 1) * hd)
            yield w, h

    return [i for i in it()]


class Widget(QWidget):

    frames = 10
    interval = 50
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._action = None
        self._frames = []

        for name in ACTIONS:
            timer = QTimer(self)
            setattr(self, '_%sTimer' % name, timer)
            QObject.connect(timer, SIGNAL('timeout()'),
                            getattr(self, 'do_'+name))

    def grow(self, size):
        self._growQueue = coord_path((self.width(), self.height()),
                                     (size.width(), size.height()),
                                     self.frames)
        self._growTimer.start(self.interval)

    def do_grow(self):
        if self._growQueue:
            w, h = self._growQueue.pop(0)
            self.resize(w, h)
        else:
            self.done('grow')

    def slide(self, point):
        self._slideQueue = coord_path((self.x(), point.x()),
                                     (self.y(), point.y()),
                                     self.frames)
        self._slideTimer.start(self.interval)

    def do_slide(self):
        if self._slideQueue:
            x, y = self._slideQueue.pop(0)
            self.move(x, y)
        else:
            self.done('slide')

    def done(self, action):
        """ Called when an action is finished. """
        pass

    def _start(self):
        self._frames = range(10)
        self._timer.killTimers()
        self._timer.start(INTERVAL)

    def _smoothTimeout(self):
        """ timer event """
        if self._action == self.SHADE:
            pass

        if self._frames:
            self._frames = self.frames[1:]
        else:
            self._timer.stop()
            self.actionDone()


if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QSize, QPoint
    a = QApplication([])
    class W(Widget):
        def mouseReleaseEvent(self, e):
            #self.grow(QSize(self.width()*2, self.height()*2))
            self.slide(QPoint(self.x()+100, self.y()+100))
            
    w = W()
    w.resize(100, 100)
    w.show()
    w.mouseReleaseEvent(None)
    a.exec_()
