#!/usr/bin/env python
#
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
import scsynth


class Time:
    value = 0
    def time(self):
        return self.value

class TempoClockTest(unittest.TestCase):

    def setUp(self):
        self.localclock = Time()
        self.clock = scsynth.TempoClock(60.0, localclock=self.localclock)

    def test_update(self):
        self.assertEqual(self.clock.beat(), 0)
        
        self.localclock.value = 1
        self.clock.update()
        self.assertEqual(self.clock.beat(), 1)
        self.assertEqual(self.clock.step(), 64)

        self.localclock.value = 3.5
        self.clock.update()
        self.assertEqual(self.clock.beat(), 3)
        self.assertEqual(self.clock.step(), 224)

        self.localclock.value = 5.1
        self.clock.update()
        self.assertEqual(self.clock.beat(), 5)
        self.assertEqual(self.clock.step(), 326)

        self.localclock.value = 11.3
        self.clock.update()
        self.assertEqual(self.clock.beat(), 11)
        self.assertEqual(self.clock.step(), 723)

    def test_time(self):
        self.assertEqual(self.clock.time(2), 2)
        self.assertEqual(self.clock.time(4.5), 4.5)

        self.localclock.value = 3
        self.assertEqual(self.clock.time(2), 2)
        self.assertEqual(self.clock.time(4.5), 4.5)

        self.localclock.value = 10
        self.assertEqual(self.clock.time(2), 2)
        self.assertEqual(self.clock.time(4.5), 4.5)

    def test_last(self):
        self.localclock.value = 1.1
        self.clock.update()
        self.assertEqual(self.clock.recent, 1)


if __name__ == '__main__':
    unittest.main()
