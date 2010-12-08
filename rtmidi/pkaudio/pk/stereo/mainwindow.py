"""
pkstereo mainwindow
"""


import os.path
from PyQt4.QtCore import QObject, SIGNAL, Qt, QSize, QPoint, QTimer
from PyQt4.QtGui import *
import pk.widgets.scrollbar
from database import Database, Item as DatabaseItem
from categories import CategoryButtons, CATEGORIES, ORDERED
from ripperwidget import RipperWidget, Mock
from transport import Transport
import ripper
from cdnotify import Drive
import mpdclient
import mpd


def Item_for_filename(filename):
    fname = filename
    item = DatabaseItem()
    item.filename = fname
    if '://' in fname:
        item.text = fname
        item.genre = 'Misc'
    else:
        tail, track = os.path.split(fname)
        genre, disc = os.path.split(tail)
        track = track.replace('.ogg', '')
        if track[2] == '_':
            track = track[3:]
        item.text = '%s - %s' % (disc, track)
        if not genre in CATEGORIES:
            genre = 'Misc'
        item.genre = genre
    return item 
    


class MainWindow(QWidget):
    """ """
    def __init__(self, parent=None):
        QWidget.__init__(self)
        Layout = QVBoxLayout(self)
        icon = QPixmap(':icons/clover.png')
        self.setWindowIcon(QIcon(icon))

        self.mpd = mpd.Mpd()
        QObject.connect(self.mpd, SIGNAL('updatePlaylist()'),
                        self.updatePlaylist)
        QObject.connect(self.mpd, SIGNAL('updateCurrentSong()'),
                        self.updateCurrentSong)    
        QObject.connect(self.mpd, SIGNAL('updateDatabase()'),
                        self.updateDatabase)

        ## UPPER STUFF

        TitleLayout = QHBoxLayout()
        Layout.addLayout(TitleLayout)
        
        self.nowPlaying = QLabel('The playlist is empty', self)
        font = QFont(self.nowPlaying.font())
        font.setPointSize(font.pointSize() * 1.5)
        self.nowPlaying.setFont(font)
        self.nowPlaying.setFixedHeight(30)
        TitleLayout.addWidget(self.nowPlaying)

        self.logo = QLabel(self)
        self.logo.setPixmap(icon)
        self.logo.setFixedSize(icon.size())
        TitleLayout.addWidget(self.logo)

        ## BUTTONS
        self.buttons = CategoryButtons(self)
        QObject.connect(self.buttons, SIGNAL('selected(QString &)'),
                        self.selectCategory)
        Layout.addWidget(self.buttons)
        
        ## DATABASE

        DatabaseLayout = QHBoxLayout()
        Layout.addLayout(DatabaseLayout)
        
        self.database = Database()
        self.database.resize(800, 600)
        QObject.connect(self.database, SIGNAL('clicked(QString &)'),
                        self.queue)
        
        self.databaseScroll = QScrollArea(self)
        self.databaseScroll.setWidget(self.database)
        self.databaseScroll.setWidgetResizable(True)
        self.databaseScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.databaseScroll.verticalScrollBar().setFixedWidth(30)
        self.databaseScroll.verticalScrollBar().setMaximum(1000)
        DatabaseLayout.addWidget(self.databaseScroll)

        self.databaseVerticalScrollBar = pk.widgets.scrollbar.ScrollPad(self)
        self.databaseVerticalScrollBar.setMinimumWidth(50)
        QObject.connect(self.databaseVerticalScrollBar,
                        SIGNAL('valueChanged(int)'),
                        self.scroll)
        DatabaseLayout.addWidget(self.databaseVerticalScrollBar)

        self._ripPool = []
        self.ripper = RipperWidget(self)
        #self.ripper = Mock(self)
        QObject.connect(self.ripper, SIGNAL('status(QEvent *)'),
                        self.ripStatus)
        QObject.connect(self.ripper, SIGNAL('foundDiscInfo()'),
                        self.showRipper)
        QObject.connect(self.ripper, SIGNAL('doneRipping()'),
                        self.hideRipper)
        QObject.connect(self.ripper, SIGNAL('canceled()'),
                        self.ripCanceled)
        Layout.addWidget(self.ripper)

        self.transport = Transport(self.mpd, self)
        Layout.addWidget(self.transport)

        try:
            self.cddrive = Drive(self)
            QObject.connect(self.cddrive, SIGNAL('audioInserted()'),
                            self.ripper.read_disc_info)
            QObject.connect(self.cddrive, SIGNAL('ejected()'),
                            self.ripper.hide)
        except IOError, e:
            # no drive
            pass

        self.selectCategory(ORDERED[0][0])

    def scroll(self, value):
        sb = self.databaseVerticalScrollBar
        db_sb = self.databaseScroll.verticalScrollBar()
        percent = sb.value() / float(sb.maximum())
        db_sb.setValue(int(percent * db_sb.maximum()))

    def showRipper(self):
        """ """
        self._ripPool = []
        self.ripper.show()

    def hideRipper(self):
        """ """
        self._ripPool = []
        self.ripper.hide()

    def ripCanceled(self):
        for item in self._ripPool:
            print 'TAKING ITEM',item.filename
            self.database.take(item)
        QTimer.singleShot(3000, self.hideRipper)

    def ripStatus(self, e):
        """ divert rip status to database items. """
        data = e.data
        tracknum = data['tracknum']
        state = data['state']
        percent = data['percent']
        trackname = data['track']
        genre = data['genre']
        album = data['album']
        artist = data['artist']

        if trackname is None:
            return

        disc = artist+' - '+album
        filename = os.path.join(genre, disc, trackname+'.ogg') # mpd db
        wavpath = os.path.join(ripper.LIBRARY, genre, disc, trackname+'.wav')
        oggpath = os.path.join(ripper.LIBRARY, genre, disc, trackname+'.ogg')
        item = self.database.find('filename', filename)
        if not item:
            if filename in [i.filename for i in self._ripPool]:
                # canceled or something
                return
            item = Item_for_filename(filename)
            self._ripPool.append(item)
            self.database.add(item)
            self.databaseScroll.ensureVisible(item.x,
                                              item.y + item.height - 1)
            print 'ADDED ITEM FOR',filename

        item.progress = percent
        
        if state == 'rip':
            item.state = 'reading...'
        elif state == 'enc':
            item.state = 'saving...'
        elif state == 'rip_error':
            item.state = 'couldn\'t read, skipped'
            print 'DELETING',wavpath
            self.database.take(item)
            self._ripPool.remove(item)
            try: os.remove(wavpath)
            except: pass
        elif state == 'enc_error':
            item.state = 'couldn\'t save, skipped'
            print 'DELETING',oggpath
            self.database.take(item)
            self._ripPool.remove(item)
            try: os.remove(oggpath)
            except: pass
        else:
            if percent == 100 and state == 'rip':
                print 'DONE READING',wavpath
                item.state = 'waiting...'
            else:
                item.state = None

        if percent == 100:
            if state == 'enc':
                if os.path.isfile(oggpath):
                    print 'ADDING FILE %s' % oggpath
                    try:
                        self.mpd.update()
                    except mpdclient.MpdError, e:
                        pass
                else:
                    print 'INVALID FILE %s' % oggpath
            item.state = None
        self.database.updateItem(item)
        
    def selectCategory(self, category):
        """ set a filter """
        category = str(category)
        if not category in CATEGORIES.keys():
            category = None
        self.database.search(category)

    ## DATA methods

    def queue(self, filename):
        """ Queue an item and ensure something's playing. """
        self.mpd.queue(str(filename))
        if self.mpd.status.stateStr() != 'play':
            self.mpd.play()

    def updateCurrentSong(self):
        #print 'MPD::updateCurrentSong'
        song = self.mpd.currentSong()
        if song:
            tail, track = os.path.split(song.path)
            genre, disc = os.path.split(tail)
            track = track.replace('.ogg', '')[3:]
            text = 'Now Playing: %s - %s' % (disc, track)
            self.nowPlaying.setText(text)
        else:
            self.nowPlaying.setText('End of playlist')
            
    def updatePlaylist(self):
        print 'MPD::updatePlaylist'
        for item in self.database.allItems():
            item.num = None
            self.database.updateItem(item)
        playlist = self.mpd.playlist()
        if playlist:
            for index, fname in enumerate(playlist):
                item = self.database.find('filename', fname)
                if item:
                    item.num = index+1
                    self.database.updateItem(item)
        else:
            for item in self.database.allItems():
                item.num = None
                self.database.updateItem(item)
            self.nowPlaying.setText('The playlist is empty')
        #self.database.update()

    def updateDatabase(self):
        print 'MPD::updateDatabase'
        # this should really delete stale items too

##         filenames = [i.filename for i in self.mpd.listdatabase()
##                      if self.database.find('filename', i.fn) is None]
##         for fname in filenames:
##             item = Item_for_filename(fname)
##             self.database.add(item)
##         self.database.search(self.database._genre)
##         return

        ## We want to remove stale entries, but not entries that are
        ## being ripped.
        existing = [i.filename for i in self.database.allItems()
                    if not i in self._ripPool]
        # clean stale ones
        filenames = self.mpd.listdatabase()
        for fn in existing:
            if not fn in filenames:
                self.database.take(self.database.find('filename', fn))
        # look for new ones
        for fn in filenames:
            if fn.endswith('.wav'): # ugg
                continue
            item = self.database.find('filename', fn)
            if item is None:
                self.database.add(Item_for_filename(fn))
        self.database.search(self.database._genre)
