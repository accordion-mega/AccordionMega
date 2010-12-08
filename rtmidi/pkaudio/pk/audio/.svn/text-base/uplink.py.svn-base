import os
import fcntl
import Queue
import socket
import select
from PyQt4.QtCore import SIGNAL, QThread


_DEBUG = False
def DEBUG(msg):
    if _DEBUG:
        print msg


class Dispatch:
    """ read a file, write a file. """
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.in_fd = infile.fileno()
        self.out_fd = outfile.fileno()
        self._buf = ''

    def run(self):
        while True:
            iwtd, owtd, ewtd = select.select([self.infile], [], [], 1)
            if iwtd:
                try:
                    ch = os.read(self.in_fd, 1)
                except OSError, e:
                    print e
                    return
            else:
                continue
            try:
                os.write(self.out_fd, ch)
            except OSError, e:
                return
            # scan for 'quit\0'
            if ch == '\0' or ch == '\n' or ch == '\r':
                _buf = self._buf
                self._buf = ''
                if _buf == 'quit':
                    return
            else:
                self._buf += ch
    def exec_(self):
        self.run()
        self.infile.close()
        self.outfile.close()

import fcntl
import threading
class Listener(threading.Thread):
    """ listen to a socket, emit delimited messages. """
    def __init__(self, infile, callback=None, parent=None):
        threading.Thread.__init__(self, parent)
        self.infile = infile
        fcntl.fcntl(infile, fcntl.F_SETFL, os.O_NONBLOCK)
        self._running = False
        self._buf = ''
        self.callback = callback
        self.queue = Queue.Queue()

    def quit(self):
        self._running = False

    def run(self):
        self.in_fd = self.infile.fileno()
        self._running = True
        while self._running:
            self._poll()

    def _poll(self):
        print 'waiting'
        iwtd, owtd, ewtd = select.select([self.infile], [], [], 1)
        if iwtd:
            try:
                ch = os.read(self.in_fd, 1)
                self._buf += ch
            except OSError, e:
                self._running = False
                return
            if ch == '\n' or ch == '\0':
                msg = self._buf.replace('\n', '').replace('\0', '').strip()
                if msg:
                    self._handle(msg)
                self._buf = ''

    def _handle(self, msg):
        if msg == 'quit':
            self._running = False
        else:
            self.queue.put(msg)
            if self.callback:
                self.callback()
            else:
                self.emit(SIGNAL('uplink'))
