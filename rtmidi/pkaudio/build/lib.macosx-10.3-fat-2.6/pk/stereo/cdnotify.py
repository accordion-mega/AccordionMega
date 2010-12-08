"""
Notification of basic cd events like insert, eject.
"""

import os
import cd_logic, CDLow
import CDROM
from PyQt4.QtCore import QObject, SIGNAL


class Drive(QObject):
    """
    SIGNALS:
        'audioInserted()'
        'dataInserted()'
        'ejected()'
    """

    INTERVAL = 250
    
    def __init__(self, parent=None, dev='/dev/cdrom'):
        QObject.__init__(self, parent)
        self._status = None
        if not os.access(dev, os.F_OK | os.R_OK):
            raise IOError('Permission denied to read %s' % dev)
        cd_logic.set_dev(dev) # no likey
        self.startTimer(self.INTERVAL)

    def timerEvent(self, e):
        """ """
        status = cd_logic.check_dev()
        if status != self._status:
            self._status = status
            self.sendUpdate()

    def sendUpdate(self):
        """ something happened. """
        if self._status in [CDROM.CDS_TRAY_OPEN, CDROM.CDS_NO_DISC]:
            self.emit(SIGNAL('ejected()'))
            
        elif self._status == CDROM.CDS_DISC_OK:
            disc_type = CDLow.get_disc_type()
            if disc_type == CDROM.CDS_AUDIO:
                self.emit(SIGNAL('audioInserted()'))
            elif disc_type in (CDROM.CDS_DATA_1, CDROM.CDS_DATA_2):
                self.emit(SIGNAL('dataInserted()'))
            else:
                print 'cdnotify: unknown disc type (%i)' % disc_type

        elif self._status == -1:
            print 'cdnotify: status -1'
            
        else:
            print 'cdnotify: unknown status (%i)' % self._status


if __name__ == '__main__':
    from PyQt4.QtCore import QCoreApplication
    a = QCoreApplication([])
    drive = Drive()

    def cb_audio():
        print 'inserted audio'
    def cb_data():
        print 'inserted data'
    def cb_eject():
        print 'ejected'
    
    QObject.connect(drive, SIGNAL('audioInserted()'),
                    cb_audio)
    QObject.connect(drive, SIGNAL('dataInserted()'),
                    cb_data)
    QObject.connect(drive, SIGNAL('ejected()'),
                    cb_eject)
    a.exec_()
    
