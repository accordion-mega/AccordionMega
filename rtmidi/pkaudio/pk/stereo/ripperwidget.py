"""
A one-button ripper widget. 
"""

import os, os.path
from PyQt4.QtCore import QObject, SIGNAL, QTimer, QEvent
from PyQt4.QtGui import QProgressBar, QApplication, QLabel, QFrame
from PyQt4.QtGui import QVBoxLayout, QPushButton, QHBoxLayout
import CDROM
import ripper
from categories import CategoryButtons, ORDERED
from smooth import Widget as SmoothWidget
import cd_logic


def event_type(i):
    return QEvent.Type(QEvent.User + i)


class RipperWidget(SmoothWidget, ripper.Ripper):
    """ One-button multi-track ripper.
    """
    def __init__(self, parent=None):
        SmoothWidget.__init__(self, parent)
        ripper.Ripper.__init__(self)
        Layout = QVBoxLayout(self)

        self.discLabel = QLabel(self)
        Layout.addWidget(self.discLabel)

        # ONLY ONE BUTTON!
        self.button = QPushButton('Cancel', self)
        self.button.setEnabled(True)
        self.button.hide()
        QObject.connect(self.button, SIGNAL('clicked()'),
                        self.cancel)
        Layout.addWidget(self.button)

        self.catFrame = QFrame(self)
        self.catFrame.setFrameStyle(QFrame.StyledPanel)
        self.catFrame.hide()
        QHBoxLayout(self.catFrame)
        self.categories = CategoryButtons(self.catFrame)
        QObject.connect(self.categories, SIGNAL('selected(QString &)'),
                        self.start)
        self.catFrame.layout().addWidget(self.categories)
        Layout.addWidget(self.catFrame)
        
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.hide()
        Layout.addWidget(self.progress)

    def start(self, category):
        """ Should already have the track info. """
        self.genre = str(category)
        self._progress_data = {}
        self.disc_length = 0.0
        for i in range(self.count):
            sec = cd_logic.get_track_time_total(i)
            self._progress_data[i] = {'rip' : 0,
                                      'enc' : 0,
                                      'length' : sec}
            self.disc_length += sec
        self.rip_n_encode()

        text = '%s - %s' % (self.artist, self.album)
        self.discLabel.setText('Copying "'+text+'"...')
        self.button.show()
        self.progress.show()
        self.catFrame.hide()
            
    def cancel(self):        
        self.stop_request = True
        path = os.path.join(ripper.LIBRARY,
                            self.genre,
                            self.artist+' - '+self.album)
        os.system('rm -rf \"%s\"' % path)
        self.discLabel.setText('Canceled')
        self.button.hide()
        self.progress.hide()
        self.progress.setValue(0)
        self.emit(SIGNAL('canceled()'))

    def read_disc_info(self):
        self.discLabel.setText('Getting disc info...')
        ripper.Ripper.read_disc_info(self)

    def ripper_event(self, e):
        """ """
        event = QEvent(event_type(e.type))
        event.data = e.__dict__
        QApplication.instance().postEvent(self, event)

    def customEvent(self, e):
        if e.type() == event_type(ripper.CDDB_DONE):
            self.button.setEnabled(True)
            text = '%s - %s' % (self.artist, self.album)
            text += '           ( Select a category... )'
            self.discLabel.setText(text)
            self.catFrame.show()
            self.emit(SIGNAL('foundDiscInfo()'))
        elif e.type() == event_type(ripper.STATUS_UPDATE):
            self.updateProgress(e.data)
            self.emit(SIGNAL('status(QEvent *)'), e)

    def updateProgress(self, data):
        """
        assume rip and enc are equal in time.
        """
        state = data['state']
        tracknum = data['tracknum']
        percent = data['percent']
        goal_percents = self.count * 200

        item = self._progress_data[tracknum]
        if state == 'rip':
            item['rip'] = percent
        elif state == 'enc':
            item['enc'] = percent
        else:
            # err, etc...
            item['rip'] = 0
            item['enc'] = 0

        total = 0
        for i, v in self._progress_data.items():
            seconds = v['length']
            rip_perc = v['rip']
            enc_perc = v['enc']

            worth = seconds / self.disc_length
            rip_perc *= worth
            enc_perc *= worth
            total += rip_perc + enc_perc
            #print i, worth, rip_perc, enc_perc, total
        percent = total / 2
        self.progress.setValue(percent)

        if percent == 100:
            if self.is_ripping:
                print 'percent == 100 but still ripping?'
            if self.is_encoding:
                print 'percent == 100 but still encoding?'
            else:
                print 'percent == 100 and ripper finished'
            self.button.hide()
            self.progress.hide()
            text = 'Finished copying \"%s - %s\"' % (self.artist, self.album)
            self.discLabel.setText(text)
            self.emit(SIGNAL('doneRipping()'))


class Mock(SmoothWidget):
    def __init__(self, parent=None):
        SmoothWidget.__init__(self, parent)
        self.percent = 0
        self.setFixedHeight(150)
        self.tid = self.startTimer(500)
        
    def read_disc_info(self):
        self.emit(SIGNAL('foundDiscInfo()'))
            
    def timerEvent(self, e):
        if self.percent == 100:
            self.killTimer(self.tid)
       
        event = QEvent(QEvent.User)
        data = {}
        data['tracknum'] = 0
        data['state'] = 'enc'
        data['percent'] = self.percent
        data['track'] = 'Banco de Patricio'
        data['genre'] = 'Christmas'
        data['album'] = 'Patricio Nino'
        data['artist'] = 'AAAorthman'
        event.data = data
        self.emit(SIGNAL('status(QEvent *)'), event)
        self.percent += 10
 

if __name__ == '__main__':
    import os.path
    ripper.LIBRARY = os.path.join(os.getcwd(), 'tests')
    a = QApplication([])
    w = RipperWidget()
    w.show()
    w.read_disc_info()
    a.exec_()
