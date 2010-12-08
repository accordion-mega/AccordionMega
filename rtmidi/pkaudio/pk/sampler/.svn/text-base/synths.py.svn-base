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
Heavy-weight synth definitions
"""

import time
from PyQt4.QtCore import QObject, SIGNAL
import scsynth


class Synth(QObject, scsynth.Synth):
    """ Container for a playing synth. """
    def __init__(self, parent=None, localclock=time):
        QObject.__init__(self, parent)
        scsynth.Synth.__init__(self)
        self.localclock = localclock
        self.notes = []
        
    def _check(self):
        """ remove old notes. """
        for start, stop in list(self.notes):
            if stop <= self.localclock.time():
                self.notes.remove((start, stop))

    def add_note(self, start, stop):
        """ """
        self.notes.append((start, stop))
        self._check()

    def clear_notes(self):
        self.notes = []

    def update(self):
        """ separate these? """
        self.emit(SIGNAL('updateSynth(QObject *)'), self)
        self.emit(SIGNAL('updateNotes(QObject *)'), self)


def midicps(note):
    return 440.0 * pow(2.0, (note - 69.0) * 0.083333333333)

def midiratio(note):
    return pow(2.0, (note - 69.0) * 0.083333333333)


class Sample(Synth):
    """ convenience class """

    name = 'JASStereoSamplePlayer'
    filetempo = None
    filepath = None
    
    def __init__(self, parent=None):
        Synth.__init__(self, parent)
        self['bufnum'] = None
        self['loopIt'] = 0
        self['rateSCale'] = 1.0

    def pitch(self, pitch):
        if self.filetempo is None:
            self['rateSCale'] = midiratio(pitch)


class Sine(Synth):

    name = 'JASSine'
    
    def __init__(self, parent=None):
        Synth.__init__(self, parent)
        self['freq'] = 440
        
    def pitch(self, pitch):
        self['freq'] = midicps(pitch)


class Munger(Synth):

    name = 'PKMunger'

    def __init__(self, parent=None):
        Synth.__init__(self, parent)
        self['buf'] = 1
        self['bufFrames'] = 44100.0
        self['grate'] = 10.0
        self['grate_var'] = 0.0
        self['glen'] = 500.0
        self['glen_var'] = 0
        self['gpitch'] = 1.0
        self['gpitch_var'] = 0.0
        self['ggain'] = 0.6
        self['ggain_var'] = 0.2
        self['direction'] = 0
        self['position'] = -1
        self['voices'] = 10
        self['pan_spread'] = 0.5
        self['smoothpitch'] = 1
        self['wrampLength'] = 512.0

    def pitch(self, pitch):
        pass



if __name__ == '__main__':
    print midicps(60)
    print midicps(61)
