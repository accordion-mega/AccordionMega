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
midi_keyboard | scsynth
"""

import scsynth


class RTPlayer:

    synth = None
    
    def __init__(self, server, verbose=False):
        self.notes = {}
        self.server = server
        self.verbose = verbose

    def note_on(self, key, vel):
        if self.synth:
            self.notes[key] = self.server.synthpool.get()
            synth = self.synth.copy()
            synth.pitch(key)
            osc = ['/s_new', synth.name, self.notes[key], 1, 0]
            for key, value in synth.items():
                osc.extend([key, value])
            self.server.sendMsg(*osc)
            if self.verbose:
                print '<<<', osc

    def note_off(self, key, vel):
        if key in self.notes:
            osc = ('/n_free', self.notes[key])
            self.server.sendMsg(*osc)
            if self.verbose:
                print '<<<', osc
            self.server.synthpool.recycle(self.notes[key])
            del self.notes[key]

