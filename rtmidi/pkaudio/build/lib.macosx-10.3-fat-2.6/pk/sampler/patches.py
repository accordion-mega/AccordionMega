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
finding, selecting and loading patches.
"""
import os
from PyQt4.QtCore import Qt
from pk.widgets import Button
from pk.audio import media
import selector

# ~/.pksampler
PATCH_DIR = os.path.join(os.environ['HOME'], '.pksampler')
LAYERS = ['bass', 'drums', 'lead', 'misc', 'pads']


def find_patches():
    subdirs = os.listdir(PATCH_DIR)
    subdirs.sort()
    patches = [i for i in subdirs
               if os.path.isdir(os.path.join(PATCH_DIR, i))]
    return patches


class PatchSelector(selector.Selector):
    def __init__(self, parent=None, orientation=Qt.Vertical):
        selector.Selector.__init__(self, parent, orientation)
        self.find_patches()

    def find_patches(self):
        self.setOptions(find_patches(), 'patch')


class Patch:

    name = None
    layers = None
    loop_beats = None
    
    def __init__(self, name):
        self.name = name
        self.homedir = os.path.join(PATCH_DIR, name)
        self.layers = {}
        self.loop_beats = {}

        for layer in LAYERS:
            self.layers[layer] = []
            lpath = os.path.join(self.homedir, layer)

            if os.path.isdir(lpath):
                self.layers[layer] = []
                for fname in os.listdir(lpath):
                    fpath = os.path.join(lpath, fname)
                    if media.supported(fpath):
                        self.layers[layer].append(fpath)

        manifest = {}
        for line in open(os.path.join(self.homedir, 'manifest')).readlines():
            key, value = line.split(' = ')
            manifest[key] = value.replace('\n', '')

        for k, v in manifest.items():
            print "MANIFEST \"%s\": %s = %s" % (name, k, v)
            if k == 'tempo':
                self.tempo = float(v)
            else:
                layer, fname = k.split('/')
                value, unit = v.split(' ')
                if unit == 'beats':
                    beats = int(value)
                    print 'BEATS: %s, %i' % (k, beats)
                    self.loop_beats[k] = beats

    def __str__(self):
        samples = 0
        for k, v in self.layers.items():
            samples += len(v)
        fmt = "Patch: \"%s\" %i samples, %0.f bpm"
        return fmt % (self.name, samples, self.tempo)


def main():
    import sys
    from PyQt4.QtCore import QObject, SIGNAL
    from PyQt4.QtGui import QApplication, QPalette, QColor
    def selected(name=None):
        if not name:
            name = w._selected
        print 'Selected:',name, Patch(name)
    a = QApplication(sys.argv)
    w = PatchSelector()
    palette = w.palette()
    palette.setColor(QPalette.Window, QColor(136, 136, 136))
    w.setPalette(palette)
    QObject.connect(w, SIGNAL('selected()'), selected)
    w.show()
    a.exec_()

                
if __name__ == '__main__':
    main()

    
