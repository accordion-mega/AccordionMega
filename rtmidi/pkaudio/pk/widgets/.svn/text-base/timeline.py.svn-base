"""
Time passes, and the sound with it.
"""

from PyQt4.QtCore import QRect, QPoint
from PyQt4.QtGui import QWidget, QPainter, QColor, QPalette, QBrush


colors = (QColor('green'),
          QColor('red'),
          QColor('blue'),
          QColor('orange'),
          QColor('purple'),
          )

def next_color():
    global colors
    c = colors[0]
    colors = colors[1:] + (colors[0],)
    return c


class Item:
    color = None
    starttime = None
    endtime = None

    def __init__(self):
        self.color = next_color()


class TimeLine(QWidget):
    """ Draw items in real-time on a scrolling beat-wise timeline. """
    
    interval = 100
    frametime = 0
    left_margin = 10
    right_margin = 10
    show_beats = 64
    bgcolor = QColor('blue')
    
    def __init__(self, clock, parent=None):
        QWidget.__init__(self, parent)
        self.clock = clock
        self.items = []
        self.frametime = 0
        self._timerid = None

    def stop(self):
        if not self._timerid is None:
            self.killTimer(self._timerid)

    def start(self):
        self.stop()
        self._timerid = self.startTimer(self.interval)
        
    def add(self, item):
        """ return a new item. """
        self.items.append(item)
        self.update()

    def x_for_frametime(self, frametime):
        """ Return a visible x value for the frame-time. """
        delta = frametime - self.frametime
        fpp = self.frames_per_pixel()
        return self.left_margin + int(delta / fpp)

    def frametime_for_x(self, x):
        w = x - self.left_margin
        f = int(float(w) * self.frames_per_pixel())
        return self.frametime + f

    def pixels_per_beat(self):
        view_width = self.width() - self.left_margin - self.right_margin
        return view_width / float(self.show_beats)
    
    def frames_per_pixel(self):
        fpb = self.clock.frames_per_beat()
        return float(fpb) / self.pixels_per_beat()

    def timerEvent(self, e):
        self.tick()

    def tick(self):
        """ scroll to current time. """
        frametime = self.clock.periodstart
        if frametime != self.frametime: # stopped?
            self.update()
            self.frametime = frametime

    def paintEvent(self, e):
        painter = QPainter(self)

        brush = QBrush(painter.brush())
        self.bgcolor.setAlpha(20)
        painter.setBrush(self.bgcolor)
        painter.drawRect(0, 0, self.width(), self.height())
        self.bgcolor.setAlpha(15)
        painter.setBrush(self.bgcolor)
        painter.drawRect(0, 20, self.width(), self.height()-40)
        painter.setBrush(brush)

        frame = self.clock.last_beat_frame
        x = self.x_for_frametime(frame)
        while x < self.width():
            x = self.x_for_frametime(frame)
            painter.drawLine(x, 0, x, 15)
            painter.drawLine(x, self.height(), x, self.height() - 15)
            #painter.drawText(QPoint(x+5, 13), str(frame))
            frame += self.clock.frames_per_beat()

        self.items = [i for i in self.items if i.endtime > self.frametime]
        for item in self.items:
            x = self.x_for_frametime(item.starttime)
            w = self.x_for_frametime(item.endtime) - x
            color = QColor(item.color)
            color.setAlpha(150)
            painter.setPen(color)
            pen = painter.pen()
            pen.setWidth(3)
            painter.setPen(pen)
            color.setAlpha(100)
            painter.setBrush(color)
            painter.drawRect(x, 0, w, self.height())


class EdittableTimeLine(TimeLine):
    """ Adds items from mouse events. """

    _draw_box = None
    snap_frames = None
    box_color = QColor('yellow')

    def __init__(self, parent=None):
        TimeLine.__init__(self, parent)
        self.setMouseTracking(False)

    def paintEvent(self, e):
        TimeLine.paintEvent(self, e)
        if self._draw_box:
            painter = QPainter(self)
            color = QColor(self.box_color)
            color.setAlpha(100)
            painter.setPen(color)
            color.setAlpha(50)
            painter.setBrush(color)
            painter.drawRect(self._draw_box)

    def snap(self, frame):
        """ snap to the closest multiple of snap_frames """
        after = self.clock.last_beat_frame
        while after < frame:
            after += self.snap_frames
        before = after - self.snap_frames
        if frame - before < after - frame:
            return before
        else:
            return after
            
    def mousePressEvent(self, e):
        self.stop()
        self._draw_box = QRect(e.x(), 0, 15, self.height())
        self.update()
        
    def mouseMoveEvent(self, e):
        x, y = self._draw_box.x(), 0
        w, h = e.x() - self._draw_box.x(), self.height()
        self._draw_box = QRect(x, y ,w, h)
        self.update()

    def mouseDoubleClickEvent(self, e):
        """ add an infinite item """

    def mouseReleaseEvent(self, e):
        if self._draw_box is None:
            return # OS X
        self.start()
        startframe = self.frametime_for_x(self._draw_box.x())
        endframe = self.frametime_for_x(e.x())
        if self.snap_frames:
            startframe = self.snap(startframe)
            endframe = self.snap(endframe)

        item = Item()
        item.starttime = startframe
        item.endtime = endframe
        self.add(item)
        self.emit(SIGNAL('newItem(int, int)'), startframe, endframe)
        self._draw_box = None
        self.update()
    

if __name__ == '__main__':
    from PyQt4.QtCore import QTimer, QObject, SIGNAL
    from PyQt4.QtGui import QApplication

    import time
    from pk.audio import flow
    app = QApplication([])
    clock = flow.MusicClock()
    clock.periodsize = 512
    timeline = EdittableTimeLine(clock)

    fpb = clock.frames_per_beat()
    for i in range(5):
        item = Item()
        item.starttime = (fpb * 2) + fpb * i
        item.endtime = item.starttime + fpb
        timeline.add(item)
    timeline.snap_frames = clock.frames_per_beat()
    timeline.show()

    pos = 0
    def slotTick():
        global pos
        clock.set(pos, clock.periodsize)
        pos += clock.periodsize
    timer = QTimer(app)
    QObject.connect(timer, SIGNAL('timeout()'), slotTick)

    def slotNewItem(start, end):
        print 'schedule event (frame %i => frame %i)' % (start, end)
    QObject.connect(timeline, SIGNAL('newItem(int, int)'), slotNewItem)

    timeline.start()
    timer.start(20)
    app.exec_()
