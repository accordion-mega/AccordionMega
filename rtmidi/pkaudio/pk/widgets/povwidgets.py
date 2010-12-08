"""
Pre-packaged povray widgets.
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPixmap, QPalette
import resources
from pk.widgets.utils import POV_COLOR
from pixmapwidgets import CyclicSlider, PixmapSlider, PixmapButton, PixmapKnob, path_for


class Button(PixmapButton):
    def __init__(self, parent=None, color='gray'):
        PixmapButton.__init__(self, parent, 'button', 17, color)
        self.palette().setColor(QPalette.Window, POV_COLOR)

class MixerSlider(PixmapSlider):
    def __init__(self, parent=None):
        PixmapSlider.__init__(self, parent, 'mixerslider', 127)
        self.setOrientation(Qt.Vertical)
        self.palette().setColor(QPalette.Window, POV_COLOR)

class VerticalWheel(CyclicSlider):
    def __init__(self, parent=None):
        CyclicSlider.__init__(self, parent, 'verticalwheel', 23)
        self.palette().setColor(QPalette.Window, POV_COLOR)

class Knob(PixmapKnob):
    def __init__(self, parent=None):
        PixmapKnob.__init__(self, parent, 'knob', 127)
        self.setValue(64)
        self.setOrientation(Qt.Vertical)
        pixmap = QPixmap(path_for('knob', 0))
        self.setMask(pixmap.createHeuristicMask())



if __name__ == '__main__':
    import utils
    utils.run_widget(Knob)
