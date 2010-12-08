#   Copyright (C) 2006 by Patrick Stinson                                 
#   patrickkidd@gmail.com                                                   
#                                                                         
#   This program is free software; you can redistribute it and/or modify  
#   it under the terms of the GNU General Public License as published by  
#   the Free Software Foundation; either version 2 of the License, or     
#   (at your option) any later version.                                   
#                                                                         
#   This program is distributed in the hope that it will be useful,       
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#   GNU General Public License for more details.                          
#                                                                         
#   You should have received a copy of the GNU General Public License     
#   along with this program; if not, write to the                         
#   Free Software Foundation, Inc.,                                       
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  
#
"""
Pattern editor

everything is in 1/64th measure
"""

import os.path
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import *
import pk.widgets
from pk.widgets.utils import POV_COLOR
import keyboard
import scsynth
import parts
import spec


HALFSTEPS = 127


def draw_note(note, painter, parent):
    _brush = QBrush(painter.brush())
    brush = QColor('red')
#    if note.selected:
#        brush = brush.dark(150)
    painter.setBrush(brush)
    mul = (64 / parent.res)
    w = (note.stop - note.start) * parent.x_px
    painter.drawRect(note.start * parent.x_px,
                     parent.height() - note.pitch * parent.y_px,
                     w,
                     parent.y_px)
    painter.setBrush(_brush)
    

class GridDisplay(QWidget):

    x_px = 1 # 1/64 beat
    y_px = 20
    res = 64 # 1 / res beats
    beats = 8
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.pattern = None
        self.set_x_px(self.x_px)
        self.set_y_px(self.y_px)
        self.set_beats(self.beats)
        self.set_res(self.res)

    def paintEvent(self, e):
        painter = QPainter(self)

        x = 0
        while x < self.width():
            painter.drawLine(x, 0, x, self.height())
            x += self.x_px * (64 / self.res)

        y = 0
        while y < self.height():
            painter.drawLine(0, y, self.width(), y)
            y += self.y_px

        if self.pattern:
            for note in self.pattern:
                draw_note(note, painter, self)

    def set_pattern(self, pattern):
        self.pattern = pattern
        self.update()

    def set_x_px(self, px):
        """ zoom """
        self.x_px = px
        self.setFixedWidth(self.x_px  * 64 * self.beats)
        self.update()

    def set_y_px(self, px):
        """ zoom """ 
        self.y_px = px
        self.setFixedHeight(HALFSTEPS * self.y_px)
        self.update()

    def set_beats(self, beats):
        """ beats should be a property of the pattern. """
        self.beats = beats
        self.set_x_px(self.x_px)
        self.update()

    def add(self, note):
        if not self.pattern is None:
            self.pattern.add(note)
            self.update()

    def delete(self, note):
        self.pattern.remove(note)
        self.update()

    def set_res(self, res):
        self.res = res
        self.update()


class PlayableGrid(GridDisplay):
    """ adds a play cursor. """

    play_cursor = 0
    cursor_color = QColor('black')

    def set_play_cursor(self, step):
        self.play_cursor = step
        self.update()

    def paintEvent(self, e):
        GridDisplay.paintEvent(self, e)
        painter = QPainter(self)
        painter.pen().setColor(self.cursor_color)
        painter.pen().setWidth(10)
        painter.setBrush(self.cursor_color)
        x = self.x_px * self.play_cursor
        painter.drawLine(x, 0, x, self.height())
        painter = None



class EdittableGrid(PlayableGrid):
    """ adds notes with mouse clicks. """

    Delete = 0
    Add = 1
    mode = Delete

    def __init__(self, parent=None):
        PlayableGrid.__init__(self, parent)
        self.setMouseTracking(False)
        self._adding_note = None

    def set_mode(self, mode):
        self.mode = mode
        
    def pitch_for(self, y):
        off = (self.height() - y)
        return off / self.y_px + 1

    def range_for(self, x):
        start = x / self.x_px
        stop = start + self.x_px / self.res
        return start, stop
    
    def note_for(self, x, y):
        if self.pattern:
            start, stop = self.range_for(x)
            pitch = self.pitch_for(y)
            for note in self.pattern:
                in_range = (start >= note.start and stop <= note.stop)
                if pitch == note.pitch and in_range:
                    return note

    def px_per_64(self):
        return self.x_px * (64 / self.res)

    def snap_x(self, x):
        return (x / self.px_per_64()) * self.px_per_64()

    def snap_64(self, x):
        return int(x / self.px_per_64())

    def snap_step(self, x):
        return self.snap_64(x) * (64 / self.res)

    def mousePressEvent(self, e):
        note = self.note_for(e.x(), e.y())
        if note:
            if self.mode == self.Add:
                note.selected = True
            elif self.mode == self.Delete:
                self.delete(note)
                self.emit(SIGNAL('deleted()'))
        else:
            start = self.snap_step(e.x())
            stop = start + (64 / self.res)
            pitch = self.pitch_for(e.y())
            self._adding_note = scsynth.Note(start=start, stop=stop,
                                             pitch=pitch)
            self.add(self._adding_note)

    def mouseMoveEvent(self, e):
        if self._adding_note:
            self._adding_note.stop = self.snap_step(e.x()) + (64 / self.res)
            self.update()

    def mouseReleaseEvent(self, e):
        if self._adding_note:
            note = self._adding_note
            self.emit(SIGNAL("added()"))
            self._adding_note = None


class PatternEditor(QFrame):

    keywidth = 25
        
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.palette().setColor(self.backgroundRole(), POV_COLOR)

        resolutions = (('1/16', 16),
                       ('1/8', 8),
                       ('1/4', 4),
                       ('1/2', 2),
                       ('1/1', 1))
        self.resolutions = dict(resolutions)
        
        self.saveButton = pk.widgets.Button(self, color='maroon')
        self.saveButton.setText('save')

        self.nameEdit = QLineEdit(self)
        self.nameEdit.setFixedSize(200, 30)
        self.nameEdit.setAutoFillBackground(True)
        self.nameEdit.palette().setColor(self.nameEdit.backgroundRole(),
                                         POV_COLOR.light(150))
        #self.nameEdit.setAlignment(Qt.AlignCenter)

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True)
        self.buttons = []
        for index, (text, res) in enumerate(resolutions):
            button = pk.widgets.Button(self)
            button.setText(text)
            button.setCheckable(True)
            self.buttonGroup.addButton(button, index)

        self.patternPart = parts.PatternPart(None, self)
    
        self.v_container = QWidget(self)
        self.keyboard = keyboard.Keyboard(self.v_container,
                                          orientation=Qt.Vertical)
        self.keyboard.keywidth = self.keywidth
        self.keyboard.setHalfSteps(HALFSTEPS)
        self.keyboard.setFixedWidth(50)
        self.keyboard.setFixedHeight(HALFSTEPS * self.keywidth)
        self.keyboard.move(0,0)
        
        self.grid = EdittableGrid(self.v_container)
        self.grid.setAutoFillBackground(True)
        self.grid.palette().setColor(self.grid.backgroundRole(),
                                     POV_COLOR.light(150))
        self.grid.set_x_px(5)
        self.grid.set_y_px(self.keywidth)
        self.grid.move(self.keyboard.width(), 0)
        self.grid.setFixedHeight(self.keyboard.height())

        self.v_container.setFixedHeight(self.keyboard.height())
        self.v_scrollarea = QScrollArea(self)
        self.v_scrollarea.setFrameShape(QFrame.StyledPanel)
        self.v_scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.v_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.v_scrollarea.setWidget(self.v_container)
        self.v_scrollarea.setWidgetResizable(True)

        self.v_scrollpad = pk.widgets.ScrollPad(self)
        self.v_scrollpad.setOrientation(Qt.Vertical)
        self.v_scrollpad.setMinimumWidth(spec.SCROLLPAD_WIDTH)
        self.v_scrollpad.set_color(spec.SCROLLPAD_COLOR)
        
        self.h_scrollpad = pk.widgets.ScrollPad(self)
        self.h_scrollpad.setOrientation(Qt.Horizontal)
        self.h_scrollpad.setMinimumHeight(spec.SCROLLPAD_WIDTH)
        self.h_scrollpad.set_color(spec.SCROLLPAD_COLOR)

        QObject.connect(self.buttonGroup, SIGNAL('buttonClicked(int)'),
                        self.set_res)
        QObject.connect(self.v_scrollpad, SIGNAL('valueChanged(int)'),
                        self.v_scroll)
        QObject.connect(self.h_scrollpad, SIGNAL('valueChanged(int)'),
                        self.h_scroll)
        QObject.connect(self.grid, SIGNAL('added()'),
                        self.patternPart.update)
        QObject.connect(self.grid, SIGNAL('deleted()'),
                        self.patternPart.update)
        QObject.connect(self.nameEdit, SIGNAL('textEdited(const QString &)'),
                        self.set_pattern_name)
        QObject.connect(self.saveButton, SIGNAL('clicked()'),
                        self.save_pattern)

        self.buttonGroup.button(1).setChecked(True)
        self.keyboard.raise_()
        self.grid.set_beats(16)
        self.set_res(1)
        self.v_scrollpad.setValue(self.v_scrollpad.maximum() / 2)

        ButtonLayout = QHBoxLayout()
        ButtonLayout.addWidget(self.saveButton)
        ButtonLayout.addWidget(self.nameEdit)
        ButtonLayout.addStretch(2)
        for i, r in enumerate(resolutions):
            ButtonLayout.addWidget(self.buttonGroup.button(i))
        ButtonLayout.addStretch(2)
        ButtonLayout.addWidget(self.patternPart)
        GridLayout = QHBoxLayout()
        GridLayout.addWidget(self.v_scrollarea)
        GridLayout.addWidget(self.v_scrollpad)
        Layout = QVBoxLayout(self)
        Layout.addLayout(ButtonLayout)
        Layout.addLayout(GridLayout)
        Layout.addWidget(self.h_scrollpad)

    def v_scroll(self, value):
        sb = self.v_scrollpad
        target_sb = self.v_scrollarea.verticalScrollBar()
        percent = sb.value() / float(sb.maximum())
        target_sb.setValue(int(percent * target_sb.maximum()))

    def h_scroll(self, value):
        sb = self.h_scrollpad
        percent = (sb.value() / float(sb.maximum())) * 100
        x = self.grid.width() * (percent / 100.0)
        self.grid.move(-x + self.keyboard.width(), 0)

    def set_res(self, index):
        button = self.buttonGroup.button(index)
        text = str(button.text())
        res = self.resolutions[text]
        self.grid.set_res(res)

    def set_pattern(self, pattern):
        self.patternPart.setData(pattern)
        self.nameEdit.setText(str(pattern.name))
        self.grid.set_pattern(pattern)

    def set_pattern_name(self, text):
        text = str(text)
        self.pattern.name = text

    def save_pattern(self):
        fname = self.grid.pattern.name+'.xml'
        fpath = os.path.join(spec.PATTERNS, fname)
        pattern.write(self.grid.pattern, fpath)


if __name__ == '__main__':
    import pk.widgets.utils
    class TestGrid(EdittableGrid):
        def __init__(self):
            EdittableGrid.__init__(self)
            self.set_play_cursor(64)
            self.set_res(16)
            self.set_mode(self.Delete)
            self.set_pattern(scsynth.Pattern())
            self.add(scsynth.Note(start=64, stop=100, pitch=12))
            self.add(scsynth.Note(start=64, stop=128, pitch=24))
            QObject.connect(self, SIGNAL('added()'), self.print_pattern)
            QObject.connect(self, SIGNAL('deleted()'), self.print_pattern)
        def print_pattern(self):
            print self.pattern
    class TestPatternEditor(PatternEditor):
        def __init__(self):
            PatternEditor.__init__(self)
            self.setMinimumHeight(1)
            self.set_pattern(scsynth.Pattern())
            QObject.connect(self.grid, SIGNAL('added()'),
                            self.print_pattern)
            QObject.connect(self.grid, SIGNAL('deleted()'),
                            self.print_pattern)
            self.resize(600, 600)
        def print_pattern(self):
            """ sheesh! """
            print self.grid.pattern
    pk.widgets.utils.run_widget(TestPatternEditor)
    #pk.widgets.utils.run_widget(TestGrid)
