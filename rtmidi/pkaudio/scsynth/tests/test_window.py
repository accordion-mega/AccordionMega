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
import unittest
import random
import scsynth
from test_tempoclock import Time


class WindowTest(unittest.TestCase):

    def setUp(self):
        self.localclock = Time()
        self.clock = scsynth.TempoClock(120, self.localclock)
        self.window = scsynth.Window(self.clock)
        self.window.lead = self.window.length = 1

    def test_no_time_gaps(self):
        random.seed()
        windows = []
        for i in range(100):
            length = random.random()
            self.localclock.value += length
            self.window.update()
            windows.append((self.window.begin, self.window.end))
            self.window.close()

        prev_end = windows[0][1]
        for begin, end in windows[1:]:
            self.assertEqual(begin - prev_end, 0)
            prev_end = end

    def test_no_step_gaps(self):
        random.seed()
        steps_out = 0
        for i in range(1000):
            length = random.random()
            self.localclock.value += length
            self.window.update()
            steps_out += self.window.steps
            self.window.close()            
        elapsed = self.localclock.value + self.window.lead + self.window.length
        steps_in = elapsed / self.window.one_step
        self.assertEqual(int(steps_in), steps_out)

    """ during processing the window must:
- start at least 'lead' in front of the current time.
- span at least 'length' seconds, to the lowest step.
- cope with time lapses between calls.
- be all inclusive.
"""
    def test_update(self):
        self.assertEqual(self.window.begin, self.window.end)
        self.assertEqual(self.window.begin, 0)

        # initial
        self.localclock.value = 1
        self.window.update()
        self.assertAlmostEqual(self.window.one_step, 0.0078125, 5)
        self.assertEqual(self.window.steps, 384)
        self.assertEqual(self.window.end, self.window.lead + self.window.length + 1)
        
        self.window.close()

        # first
        self.localclock.value = 1.1
        self.window.update()
        self.assertEqual(self.window.steps, 12)
        self.assertAlmostEqual(self.window.end, 3.09375, 5)
        end = self.window.begin + self.window.steps * self.window.one_step
        self.assertEqual(self.window.end, end)
        self.assertAlmostEqual(self.window.one_step, 0.0078125, 5)

        self.window.close()

        # second (scaled tempo)
        self.window.tempoclock.set_tempo(150)
        self.localclock.value = 1.2
        self.window.update()
        end = self.window.begin + self.window.steps * self.window.one_step
        self.assertEqual(self.window.end, end)
        self.assertAlmostEqual(self.window.one_step, 0.00625, 5)
        self.assertEqual(self.window.steps, 17)

        self.window.close()

        # third (jump)
        self.localclock.value = 4.5
        self.window.update()
        end = self.window.begin + self.window.steps * self.window.one_step
        self.assertEqual(self.window.end, end)
        self.assertEqual(self.window.steps, 527)
        self.assertAlmostEqual(self.window.one_step, 0.00625, 5)


if __name__ == '__main__':
    unittest.main()
