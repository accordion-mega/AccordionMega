"""
Mpd functions
"""


from PyQt4.QtCore import QObject, SIGNAL, QTimer
import mpdclient


class Mpd(QObject):
    """
    QObject wrapper, emits status updates. This is for apps that want
    to stay in sync with the server all the time (should include
    almost all) Check attributes at any time, otherwise wait for
    signals.
    """
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.pollTimer = QTimer(self)
        QObject.connect(self.pollTimer, SIGNAL('timeout()'), self.poll)

        self.controller = None
        self.status = mpdclient.Status()
        self.stats = mpdclient.Stats()
        self.status.state = 0

    def connectToHost(self, host='localhost', port=6600):
        self.controller = mpdclient.MpdController(host, port)
        self.pollTimer.start(500)
        self.poll()

    def disconnect(self):
        self.controller = None
        self.status = mpdclient.Status()
        self.stats = mpdclient.Stats()
        self.pollTimer.stop()
        
    def poll(self):
        status = self.controller.status()
        stats = self.controller.stats()

        if status.volume != self.status.volume:
            self.emit(SIGNAL('volumeUpdated(int)'), status.volume)
            
        if status.repeat != self.status.repeat:
            self.emit(SIGNAL('repeatUpdated(int)'), status.repeat)
            
        if status.random != self.status.random:
            self.emit(SIGNAL('randomUpdated(int)'), status.random)

        if status.state != self.status.state:
            self.emit(SIGNAL('stateUpdated(int)'), status.state)

        if status.totalTime != self.status.totalTime:
            self.emit(SIGNAL('timeUpdated(int, int)'),
                      status.elapsedTime, status.totalTime)

        state_str = status.stateStr()
        old_state_str = self.status.stateStr()
        if status.song != self.status.song or \
           old_state_str == 'stop' and state_str == 'play' or \
           old_state_str == 'unknown' and state_str == 'play':        
            self.emit(SIGNAL('updateCurrentSong()'))

        if stats.db_update != self.stats.db_update:
            self.emit(SIGNAL('updateDatabase()'))

        if status.playlist != self.status.playlist:
            self.emit(SIGNAL('updatePlaylist()'))

        self.status = status
        self.stats = stats


    ## BASIC ACCESSORS

    def listdatabase(self):
        return self.controller.listall('/')

    def update(self):
        self.controller.update()

    def queue(self, fname):
        self.controller.add([fname])

    def playlist(self):
        """ return a list of filenames. """
        return [song.path for song in self.controller.playlist()]

    def currentSong(self):
        """ return """
        return self.controller.getCurrentSong()

    def play(self):
        self.controller.play(self.status.song)

    def pause(self):
        self.controller.pause()

    def next(self):
        self.controller.next()

    def clear(self):
        self.controller.clear()

    def random(self):
        self.controller.random()

    def repeat(self):
        self.controller.repeat()

