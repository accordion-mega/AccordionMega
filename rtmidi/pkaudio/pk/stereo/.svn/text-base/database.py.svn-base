"""
Music database view
"""

import os
from PyQt4.QtCore import QObject, SIGNAL, QString, QSize, QRect, Qt
from PyQt4.QtGui import QPainter, QColor, QBrush, QPen, QFont
from pk.widgets import PKWidget
from categories import CATEGORIES


class Item:
    """ Used for drawing """
    genre = ''
    album = ''
    text = ''
    filename = ''
    num = None     # number in the box
    progress = 100 # progress related to state
    state = None   # text related to progress

    # drawing
    x = 0
    y = 0
    height = 30

    def color(self):
        return CATEGORIES[self.genre]


def cmd_fname(a, b):
    if a.filename > b.filename:
        return 1
    elif a.filename < b.filename:
        return -1
    else:
        return 0


class Collection:
    """ caches unique entries for sorting, etc. """
    _all = []
    _genres = {}
    
    def add(self, item):
        genre = item.genre
        self._all.append(item)
        if not genre in self._genres:
            self._genres[genre] = [item]
        else:
            # insert item
            genre = self._genres[item.genre]
            if item.filename < genre[0].filename:
                genre.insert(0, item)
            elif item.filename > genre[-1].filename:
                genre.append(item)
            else:
                prev = genre[0]
                for i, cur in enumerate(genre[1:]):
                    if i and item.filename > prev.filename and item.filename < cur.filename:
                        genre.insert(i+1, item)
                        break

    def take(self, item):
        self._all.remove(item)
        self._genres[item.genre].remove(item)

    def allItems(self):
        return self._all

    def find(self, key, value):
        for i in self._all:
            if getattr(i, key) == value:
                return i

    def by_genre(self, genre):
        try:
            return self._genres[genre]
        except KeyError:
            return []



class Database(PKWidget, Collection):
    """ Collects items. """
    
    def __init__(self, parent=None):
        PKWidget.__init__(self, parent)
        self._shown = []
        self._genre = ''
        self.padding = 2

    def add(self, item):
        Collection.add(self, item)
        if self._genre == item.genre:
            self.search(self._genre)

    def take(self, item):
        Collection.take(self, item)
        if item.genre == self._genre:
            self.search(self._genre)

    def itemAt(self, x, y):
        """ return an item at a corrdinate. """
        for item in self._shown:
            if y >= item.y and y < item.y + item.height:
                return item            

    def mouseReleaseEvent(self, e):
        item = self.itemAt(e.x(), e.y())
        if item:
            self.emit(SIGNAL('clicked(QString &)'), QString(item.filename))

    def _arrangeShown(self):
        y = 1
        for item in self._shown:
            item.y = y
            item.x = 0
            item.width = self.width()
            y += item.height + self.padding
        self.setFixedHeight(y)

    def search(self, genre):
        """ show all items matching genre. """
        self._genre = genre
        self.set_background(CATEGORIES[self._genre].dark(120))
        self._shown = self.by_genre(genre)
        self._arrangeShown()
        self.update()

    def updateItem(self, item):
        self.update(0, item.y, self.width(), item.height)

    def paintEvent(self, e):
        """ """
        PKWidget.paintEvent(self, e)

        painter = QPainter(self)
        orig_pen = QPen(painter.pen())
        orig_brush = QBrush(painter.brush())
        orig_font = QFont(painter.font())
        metrics = painter.fontMetrics()
        f_height = metrics.ascent()
        text_flags = Qt.AlignHCenter | Qt.AlignVCenter
        
        region = e.region()
        for item in self._shown:
            font_y = item.y + item.height / 2 + f_height / 2

            item_rect = QRect(0, item.y, self.width(), item.height)
            if not region.contains(item_rect):
                continue

            painter.setFont(orig_font)

            # background
            pen = item.color().dark(110)
            pen.setAlpha(100)
            painter.setBrush(QBrush(item.color()))
            painter.setPen(QPen(pen))
            w = self.width() * (item.progress * .01)
            rect = QRect(0, item.y, w, item.height)
            painter.drawRect(rect)

            # queue pos
            pen = pen.dark(140)
            pen.setAlpha(255)
            painter.setPen(QPen(pen))
            queue_rect = QRect(self.padding, item.y + self.padding,
                               item.height - self.padding * 2,
                               item.height - self.padding * 2)
            painter.drawRoundRect(queue_rect, 35, 35)

            # num
            if not item.num is None:
                painter.setPen(orig_pen)
                painter.setBrush(orig_brush)
                painter.drawText(queue_rect, text_flags, str(item.num))

            # text
            painter.setPen(orig_pen)
            painter.setBrush(orig_brush)
            font = QFont('Utopia, Italic', 14, -1, True)
            painter.setFont(font)
            rect = QRect(item_rect)
            rect.setX(item.height + self.padding * 2)
            rect.setWidth(rect.width() - rect.x())
            painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, item.text)

            # state
            if item.state:
                font = QFont('7th Service Expanded Italic, Italic')
                font.setPointSize(18)
                pen = QColor(orig_pen.color())
                pen.setAlpha(50)
                painter.setPen(QPen(pen))
                painter.setFont(font)
                x = item.x
                y = item.y
                w = self.width()
                h = item.height
                rect = QRect(x, y, w, h)
                flags = Qt.AlignVCenter | Qt.AlignRight
                painter.drawText(rect, flags, item.state+'  ')



if __name__ == '__main__':
    import random
    from categories import ORDERED
    from PyQt4.QtGui import QApplication
    a = QApplication([])
    w = Database()
    w.show()
    w.search('Classical')
    items = []
    for i in range(300):
        genre = random.choice(ORDERED)[0]
        for j in range(10):
            album = str(random.random())
            track = str(random.random())
            name = os.path.join(genre, album, track)
            item = Item()
            item.filename = name
            item.genre = genre
            item.text = '%s - %s' % (album, track)
            item.num = i + j
            item.state = 'rip'
            items.append(item)
    print 'ADDING %i ITEMS...' % len(items)
    for item in items:
        w.add(item)
    w.search('Classical')
    a.exec_()
    
