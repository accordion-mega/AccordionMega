import sys
import os


class Client:

    def __init__(self, outfile=sys.stdout):
        self.outfile = outfile
        self.fd = outfile.fileno()
    
    def __del__(self):
        os.write(self.fd, 'quit\n')

    def start(self):
        pass

    def send(self, msg):
        os.write(self.fd, msg+'\n')

    def quit(self):
        self.send('quit')

    def load(self, fpath):
        self.send('load %s' % fpath)

    def add_event(self, fpath, start, stop):
        self.send('add_event %s %s %s' % (fpath, start, stop))

    def clear_events(self, fpath):
        self.send('clear_events %s' % fpath)

    def add_to_channel(self, fpath, channel):
        self.send('add_to_channel %s %s' % (fpath, channel))

    def set_volume(self, channel, left, right):
        self.send('set_volume %s %s %s' % (channel, left, right))

    def set_looping(self, fpath, on):
        self.send('set_looping %s %s' % (fpath, on))

    def set_tempo(self, tempo):
        self.send('set_tempo %s' % tempo)

    def set_loop_beats(self, fpath, beats):
        self.send('set_loop_beats %s %s' % (fpath, beats))


if __name__ == '__main__':
    import time
    client = Client()
    CLICK = '/Users/patrick/.pksampler/click.wav'
    CLIMAX = '/Users/patrick/.pksampler/birdman/lead/climax.wav'
    client.add_to_channel(CLIMAX, 0)
    client.add_event(CLIMAX, 50000, 0)
    client.clear_events(CLICK)
    client.set_volume(0, .5, .5)

    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    app = QApplication([])
    slider = QSlider()
    slider.setRange(0, 100)
    slider.show()

    def volume(value):
        client.set_volume(0, value / 100.0, value / 100.0)
    QObject.connect(slider, SIGNAL('valueChanged(int)'), volume)
    
    app.exec_()
