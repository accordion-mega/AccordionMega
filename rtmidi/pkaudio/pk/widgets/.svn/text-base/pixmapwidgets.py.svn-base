"""
Widgets for using pixmaps 
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

ANIMATION_COEF = 2
NUM_CLOCK_DIGITS = 10

pixmap_cache = {}


def build_cache(names):
    """ Validate and cache the pixmaps. """
    for name in names:
        pixmap = QPixmap(name)
        if pixmap.isNull():
            raise IOError('invalid pixmap: %s' % name)
        lastsize = None
        if lastsize is None or pixmap.size() == lastsize:
            lastsize = pixmap.size()
            pixmap_cache[name] = pixmap
        else:
            raise ValueError('mismatched pixmap sizes (%i, %i) != (%i, %i)' %
                             (pixmap.width(), pixmap.height(),
                              lastsize.width(), lastsize.height()))


def path_for(name, index):
    """ Return a resource path for a widget's index. """
    template = ':/povray/widgets/%s/%s%s.png'
    return template % (name, name, str(index).zfill(NUM_CLOCK_DIGITS))


def list_pixmaps(name, num):
    """ Build a list of pixmap names for a widget. """
    return [path_for(name, i) for i in range(num)]
            

def cache_name(name, num):
    """ Cache for a widget's pixmaps. """
    num += 1
    build_cache(list_pixmaps(name, num))


def paint(name, index, painter):
    """ Paint a widget using a pixmap. """
    path = path_for(name, index)
    pixmap = pixmap_cache[path]
    painter.drawPixmap(QPoint(0, 0), pixmap)
    painter.end()
    

class PixmapButton(QAbstractButton):
    """ Takes bitmaps, animates clicks, and can change colors. """
    
    AnimRes = 50
    frames = 3
    
    def __init__(self, parent=None, name='button',
                 num=17, color='gray', text=None):
        """ """
        QAbstractButton.__init__(self, parent)
        white = QColor('white')
        white.setAlpha(220)
        self.palette().setColor(QPalette.WindowText, white)

        self.name = name
        cache_name(name, num)
        p = pixmap_cache[path_for(name, 0)]
        self.setFixedSize(p.size())

        self.animTimer = QTimer(self)
        QObject.connect(self.animTimer, SIGNAL("timeout()"),
                        self.slotAnimTimer)
        self.animIndex = 0
        self.animDirection = 'down'  ## ['down','down_up', 'up']
        
        QObject.connect(self, SIGNAL('toggled(bool)'), self.slotToggled)

        self.setColor(color.lower())
        self._setPixmap(self.animIndex + self.colorOffset)
        if not text is None:
            self.setText(text)

    def animate(self):
        """ Set self.animDirection then call this. """
        self.animTimer.stop()
        if self.animDirection == 'up':
            self.animIndex = 2
        else:
            self.animIndex = 0
        self.slotAnimTimer()
        self.animTimer.start(PixmapButton.AnimRes)

    def _setPixmap(self, i):
        self.pixmap_index = i
        self.update()

    def paintEvent(self, e):
        paint(self.name, self.pixmap_index, QPainter(self))
        painter = QPainter(self)
        pen = QPen(painter.pen())

        off = self.pixmap_index == self.colorOffset + 2 and 1 or 0

        painter.setPen(QColor('black'))
        
        rect = QRectF(off, off, self.width(), self.height())
        painter.drawText(rect, 0 | Qt.AlignCenter, self.text())

        painter.setPen(QColor('white'))
        rect = QRectF(1+off, 1+off, self.width()-1, self.height()-1)
        painter.drawText(rect, 0 | Qt.AlignCenter, self.text())
        
    def setColor(self, color):
        self.color = color
        colors = {'white' : 0,
                  'gray' : self.frames,
                  'black' : self.frames * 2,
                  'maroon' : self.frames * 3,
                  'green' : self.frames * 4,
                  'purple' : self.frames * 5,
                  }
        if color in colors.keys():
            self.colorOffset = colors[color]
        else:
            self.colorOffset = 0
            msg = '\'%s\' not found, available colors: %s' % (color,
                                                              colors.keys())
            raise KeyError(msg)
    
    def slotAnimTimer(self):
        if self.animDirection == 'down':
            if self.animIndex < self.frames:
                self._setPixmap(self.animIndex + self.colorOffset)
                self.animIndex += 1
            else:
                self.animTimer.stop()
            
        elif self.animDirection == 'up':
            if self.animIndex >= 0:
                self._setPixmap(self.animIndex + self.colorOffset)
                self.animIndex -= 1
            else:
                self.animTimer.stop()
                
        elif self.animDirection == 'down_up':
            if self.animIndex < self.frames:
                self._setPixmap(self.animIndex + self.colorOffset)
                self.animIndex += 1
            elif self.animIndex == self.frames:
                self.animDirection = 'up'
                self.animIndex = 2

    def mousePressEvent(self, e):
        if not self.isCheckable():
            self.animDirection = 'down'
            self.animatePress()
        QAbstractButton.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e=None):
        if not self.isCheckable():
            self.animDirection = 'up'
            self.animateRelease()
        if e != None:
            QAbstractButton.mouseReleaseEvent(self, e)
        
    def slotToggled(self, a0):
        if self.isChecked():
            self.animatePress()
        else:
            self.animateRelease()

    def setOn(self, on):
        if on:
            self.animatePress()
        else:
            self.animateRelease()
        QAbstractButton.setOn(self, on)
    
    ## ANIMATE METHODS
    
    def animateClick(self):
        self.animDirection = 'down_up'
        self.animate()
        
    def animatePress(self):
        self.animDirection = 'down'
        self.animate()
        
    def animateRelease(self):
        self.animDirection = 'up'
        self.animate()


class PixmapSlider(QAbstractSlider):
    """ A slider drawn with pixmaps"""
    
    AnimRes = 10
    
    def __init__(self, parent, name, num):
        QAbstractSlider.__init__(self, parent)
        
        cache_name(name, num)
        p = pixmap_cache[path_for(name, 0)]
        self.setFixedSize(p.size())
        self.setRange(0, num)
        self.setMouseTracking(False)

        self.name = name
        self.animated = False

        self.animFrames = []
        self.animTimer = QTimer(self)
        QObject.connect(self.animTimer, SIGNAL("timeout()"), self.slotAnim)

    def mousePressEvent(self, e):
        self.mouseMoveEvent(e)

    def mouseMoveEvent(self, e):
        """ these mixerslider-specifics need to go away! """
        margin = 5
        y = self.height() - e.y() 
        if self.orientation() == Qt.Vertical:
            if y > self.height() - margin:
                v = self.maximum()
            elif y < margin:
                v = self.minimum()
            else:
                v = ((y - 15.0) / (self.height() - 30.0)) * self.maximum()
        else:
            if e.x() > self.width() - margin:
                v = self.maximum()
            elif e.x() < margin:
                v = self.minimum()
            else:
                v = ((e.x() - 15.0) / (self.width() - 30)) * self.maximum()
        self.setValue(v)

    def paintEvent(self, e):
        pixmap = self.value()
        if self.invertedAppearance():
            pixmap = self.maximum() - self.value()
        paint(self.name, pixmap, QPainter(self))

    def wheelEvent(self, e):
        self.setValue(self.value() + e.delta())
        
    def setValue(self, new_val):
        """ Moves/Animates the control into position, sets the value. """
        new_val = int(new_val)
        if not self.animated:
            QAbstractSlider.setValue(self, new_val)
            self.update()
        else:
            if self.animTimer.isActive():
                self.animTimer.stop()
                
            # find the speed ranges
            old_val = self.value()
            travel = (new_val - old_val)
            if new_val > old_val:
                fast_end = old_val + int(travel * .6)
                slow_end = old_val + int(travel * .75)
            else:
                fast_end = old_val - int(travel * .6)
                slow_end = old_val - int(travel * .75)
                
            # calculate the animation frames
            self.animFrames = []
            current = old_val
            if new_val > old_val:
                while current < new_val:
                    if current < fast_end:
                        current += 4 * ANIMATION_COEF
                    elif current < slow_end:
                        current += 2 * ANIMATION_COEF
                    else:
                        current += 1 * ANIMATION_COEF
                    if current > new_val:
                        current = new_val
                    self.animFrames.append(current)
            else:
                while current > new_val:
                    if current > fast_end:
                        current -= 4 * ANIMATION_COEF
                    elif current > slow_end:
                        current -= 2 * ANIMATION_CEOF
                    else:
                        current -= 1 * ANIMATION_COEF

                    if current < new_val:
                        current = new_val
                    self.animFrames.append(current)

            if self.animFrames:
                self.slotAnim()
                if self.animFrames:
                    self.animTimer.start(PixmapSlider.AnimRes)

    def slotAnim(self):
        """ Process the next animation frame. """
        QAbstractSlider.setValue(self, self.animFrames.pop(0))
        if not self.animFrames:
            self.animTimer.stop()
        

class CyclicSlider(QAbstractSlider):
    """ Good for wheels, and other controls that use relative values.
    """

    delta = 0
    
    def __init__(self, parent, name, num):
        QAbstractSlider.__init__(self, parent)
        if name:
            cache_name(name, num)
            p = pixmap_cache[path_for(name, 0)]
            self.setFixedSize(p.size())

        self.name = name
        self.setRange(0, num)
        self.setSingleStep(1)
        self.setPageStep(5)
        self.setValue(0)
        self.name = name
        self.pixmapIndex = self.value()
        self.setMouseTracking(False)

    def paintEvent(self, e):
        paint(self.name, self.maximum() - self.pixmapIndex, QPainter(self))
        
    def mousePressEvent(self, e):
        self.last_y = None
        
    def mouseReleaseEvent(self, e):
        self.last_y = None
        
    def mouseMoveEvent(self, e):
        """ Just take the differences """
        # first move since press
        if self.last_y == None:
            self.last_y = e.y()

        # do the move
        else:
            delta = self.last_y - e.y()
            delta /= 2

            if delta == 0: # comeoon...gimme at least one..
                delta = 1

            # cycle pixmaps
            p_range = self.maximum() - self.minimum()
            p_delta = delta
            if delta < -p_range:
                p_delta = (abs(delta) % p_range) * -1
            elif delta > p_range:
                p_delta = delta % p_range

            index = self.pixmapIndex
            # advance the pixmap index
            if index + p_delta > self.maximum():
                index = (index + p_delta) - self.maximum()
            # loop down
            elif index + p_delta < 0:
                index = self.maximum() + (index + delta)
            # just advance the pointer
            else:
                index += p_delta

            # This range control is inversed, and there is no zero index,
            # so advance it over the max value
            if index == self.maximum():
                index = 0
            self.pixmapIndex = index

            self.emit(SIGNAL('moved(int)'), delta)
            self.delta = delta
            self.last_y = e.y()

        self.update()

    def setValue(self, new_val):
        """ We don't store values. """
        pass


class PixmapKnob(QAbstractSlider):
    """ A knob drawn with pixmaps"""
    
    def __init__(self, parent, name, num):
        QAbstractSlider.__init__(self, parent)
        self.setInvertedControls(True)
        
        cache_name(name, num)
        p = pixmap_cache[path_for(name, 0)]
        self.setFixedSize(p.size())
        self.setRange(0, num)
        self.setMouseTracking(False)

        self.name = name
        self._value = 0.0

    def mousePressEvent(self, e):
        self._last_point = (e.x(), e.y())
        self._value = self.value()

    def mouseMoveEvent(self, e):
        if self.orientation() == Qt.Vertical:
            diff = e.y() - self._last_point[1]
        else:
            diff = e.x() - self._last_point[0]
        diff = float(diff)
        if self.invertedControls():
            diff *= -1
        self._last_point = (e.x(), e.y())
        self._value = self._value + diff
        if self._value > self.maximum():
            self._value = self.maximum()
        elif self._value < self.minimum():
            self._value = self.minimum()
        self.setValue(self._value)
        self.update()

    def paintEvent(self, e):
        paint(self.name, self.value(), QPainter(self))

    def wheelEvent(self, e):
        self.setValue(self.value() + e.delta())

