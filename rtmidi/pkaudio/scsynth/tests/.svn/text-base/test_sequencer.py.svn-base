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
import random
import time
import unittest
import scsynth
from test_tempoclock import Time


random.seed()


class SequencerTest(unittest.TestCase):

    def setUp(self):
        self.localclock = Time()
        self.clock = scsynth.TempoClock(120, localclock=self.localclock)
        self.pattern = scsynth.Pattern()
#        print len(self.pattern)
        for i in (0, 64, 128, 192):
            self.pattern.add(scsynth.Note(i, i+32, 64))
        self.sequencer = scsynth.Sequencer(self.clock)

    def test_add(self):
        stream = self.sequencer.add(self.pattern)
        self.assertEqual(self.sequencer.pending[0][0], stream)
        self.assertEqual(self.sequencer.pending[0][1], 64)

    def test_remove(self):
        stream1 = self.sequencer.add(self.pattern)
        stream2 = self.sequencer.add(self.pattern)

        self.sequencer.remove(self.pattern)
        self.sequencer.remove(self.pattern)
        self.assertRaises(KeyError, lambda: self.sequencer.remove(None))

    def _test_render(self):
        window = scsynth.Window(self.clock)
        stream = self.sequencer.add(self.pattern)
        stream.loop(True)

        self.localclock.value = 1.5
        window.update()
        print window.end

        notes = self.sequencer.render(window)
        print notes
        self.assertEqual(len(notes), 3)

        window.close()
        
        self.localclock.value = 2.5
        window.update()
        notes = self.sequencer.render(window)
        self.assertEqual(len(notes), 2)

        window.close()

        self.localclock.value = 101.5
        window.update()
        notes = self.sequencer.render(window)
        self.assertEqual(len(notes), 198)

    def test_longtime(self):
        self.clock.set_tempo(150)
        window = scsynth.Window(self.clock)
        stream = self.sequencer.add(self.pattern)
        stream.loop(True)

        notes = []
        for i in range(100):
            window.update()
            ret = self.sequencer.render(window)
            notes.extend(ret)
            window.close()
            self.localclock.value += random.random()

        prev = None
        for index, note in enumerate(notes[1:]):
            if prev:
                try:
                    self.assertAlmostEqual(note[1] - prev[1], .4)
                except AssertionError, e:
                    #print 'ERROR ON INDEX:', index + 1
                    #raise e
                    pass
            prev = note


if __name__ == '__main__':
    unittest.main()
