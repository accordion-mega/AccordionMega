"""
Simple transport control.
"""

import sys
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QFrame, QPushButton, QHBoxLayout, QApplication


class Transport(QFrame):
    def __init__(self, mpd, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameStyle(QFrame.StyledPanel)
        Layout = QHBoxLayout(self)

        self.clearButton = QPushButton('Clear', self)
        self.clearButton.setFixedHeight(40)
        QObject.connect(self.clearButton, SIGNAL('clicked()'),
                        mpd.clear)
        Layout.addWidget(self.clearButton)

        self.playButton = QPushButton('Play', self)
        self.playButton.setFixedHeight(40)
        QObject.connect(self.playButton, SIGNAL('clicked()'),
                        mpd.play)
        Layout.addWidget(self.playButton)

        self.pauseButton = QPushButton('Pause', self)
        self.pauseButton.setFixedHeight(40)
        QObject.connect(self.pauseButton, SIGNAL('clicked()'),
                        mpd.pause)
        Layout.addWidget(self.pauseButton)

        self.nextButton = QPushButton('Next', self)
        self.nextButton.setFixedHeight(40)
        QObject.connect(self.nextButton, SIGNAL('clicked()'),
                        mpd.next)
        Layout.addWidget(self.nextButton)

        self.randomButton = QPushButton('Random', self)
        self.randomButton.setCheckable(True)
        self.randomButton.setFixedHeight(40)
        QObject.connect(self.randomButton, SIGNAL('toggled(bool)'),
                        mpd.random)
        QObject.connect(mpd, SIGNAL('randomUpdated(int)'),
                        self.randomButton.setDown)
        Layout.addWidget(self.randomButton)

        self.repeatButton = QPushButton('Repeat', self)
        self.repeatButton.setCheckable(True)
        self.repeatButton.setFixedHeight(40)
        QObject.connect(self.repeatButton, SIGNAL('toggled(bool)'),
                        mpd.repeat)
        QObject.connect(mpd, SIGNAL('repeatUpdated(int)'),
                        self.repeatButton.setDown)
        Layout.addWidget(self.repeatButton)

        self.exitButton = QPushButton('exit', self)
        self.exitButton.setFixedHeight(40)
        QObject.connect(self.exitButton, SIGNAL('clicked()'),
                        QApplication.instance().quit)
        Layout.addWidget(self.exitButton)
