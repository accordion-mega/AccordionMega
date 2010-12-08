
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pk.widgets import PKWidget


class PeakMeter(PKWidget):

    _interval = 75
    _timer = None

    def __init__(self, parent=None, levelbus=None):
        PKWidget.__init__(self, parent)
        self.setFrameShape(QFrame.Panel)
        self.set_background(QColor(151, 169, 0))
        self._foreground = QColor(58, 58, 58)
        
        self.levels = None
        self.levelbus = levelbus
        
        self.set_interval(self._interval)
        self.restart()

    def set_interval(self, ms):
        """ the amount of time between signals. """
        self._interval = ms
        self.restart()

    def restart(self):
        self.stop()
        if self.levelbus:
            self._timer = self.startTimer(self._interval)

    def stop(self):
        if not self._timer is None:
            self.killTimer(self._timer)

    def timerEvent(self, e):
        """ rms, peak, decay """
        self.levels = {'rms' : self.levelbus.rms,
                       'peak' : self.levelbus.peak,
                       'decay' : self.levelbus.decay }
        self.update()

    def paintEvent(self, e):
        PKWidget.paintEvent(self, e)
        painter = QPainter(self)

        if not self.levels:
            return

        pen = QPen(self._foreground.dark(150))
        gradient = QLinearGradient(QPointF(0, 100), QPointF(0, 150))
        gradient.setColorAt(0, self._foreground)
        gradient.setColorAt(1, self._foreground.light(150))
        brush = QBrush(gradient)

        w = int(self.width() / 3.5)        
        levels = self.levels
        channels = 2 # more channels later
        for i in range(channels):
            rms = levels['rms'][i]
            peak = levels['peak'][i]
            decay = levels['decay'][i]
            x = (w / 2) + int(w * 1.5 * i)
            h = self.height()

            painter.setBrush(brush)
            painter.setPen(pen)
            
            # peak
            painter.drawRect(x, h - (h * peak), w, h)

            # decay
            y = h - (h * decay)
            painter.drawLine(x, y, x + w, y)

            # rms
            painter.setBrush(QColor(100, 100, 100, 100))
            painter.setPen(QColor(200, 200, 200, 50))
            painter.drawRect(x, h - (h * rms), w, h)

             

    ###
    ### TEST FUNCTIONS
    ###
    
    def toggle_autoPreview(self):
        """ This should go away. """
        def timeout(self):
            """ Make the levels go all crazy-like """
            import random
            rms = [random.random(), random.random()]
            peak = [random.random(), random.random()]
            delay = [random.random(), random.random()]
            self.set(rms, peak, delay)

        if not hasattr(self, '__auto_timer'):
            self.__auto_timer = QTimer(self)
            QObject.connect(self.__auto_timer, SIGNAL('timeout()'),
                            timeout)
        if self.__auto_timer.isActive():
            self.__auto_timer.stop()
        else:
            self.__auto_timer.start(100)



