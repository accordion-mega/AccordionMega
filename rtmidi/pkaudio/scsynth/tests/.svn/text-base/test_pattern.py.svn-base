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
from scsynth import pattern


class XmlTest(unittest.TestCase):
    
    def test_write_read(self):
        notes = [pattern.Note(i, i+16, 64) for i in (0, 24, 64, 128, 192)]
        p1 = pattern.Pattern(notes)
        p1.name = 'mypattern'
        p1.beats = 2
        
        pattern.write(p1, 'bleh.xml')
        p2 = pattern.read('bleh.xml')

        self.assertEqual(len(p1), len(p2))
        self.assertEqual(p1.name, p2.name)
        self.assertEqual(p1[0], p2[0])
        self.assertEqual(p1[1], p2[1])
        self.assertEqual(p1[2], p2[2])
        self.assertEqual(p1[3], p2[3])
        self.assertEqual(p1[4], p2[4])


class PatternTest(unittest.TestCase):

    def test_shared_data(self):
        p = pattern.Pattern([pattern.Note(0, 1, 2)])
        self.assertEqual(len(p), 1)
        
        p = pattern.Pattern()
        self.assertEqual(len(p), 0)
        
        p = pattern.Pattern()        
        p.add(pattern.Note(0, 0, 0))
        self.assertEqual(len(p), 1)
        
        p.add(pattern.Note(1, 1, 1))
        self.assertEqual(len(p), 2)

        p = pattern.Pattern()
        self.assertEqual(len(p), 0)
                
    def test_add(self):
        """ sort all on add """
        self.pattern = pattern.Pattern()
        
        self.pattern.add(pattern.Note(192, 10, 0))
        self.assertEqual(self.pattern[0].start, 192)

        self.pattern.add(pattern.Note(67, 10, 0))
        self.assertEqual(self.pattern[0].start, 67)
        self.assertEqual(self.pattern[1].start, 192)

        self.pattern.append(pattern.Note(60, 10, 0))
        self.assertEqual(self.pattern[0].start, 67)
        self.assertEqual(self.pattern[1].start, 192)
        self.assertEqual(self.pattern[2].start, 60)

        self.pattern.add(pattern.Note(190, 10, 0))
        self.assertEqual(self.pattern[0].start, 60)
        self.assertEqual(self.pattern[1].start, 67)
        self.assertEqual(self.pattern[2].start, 190)
        self.assertEqual(self.pattern[3].start, 192)



if __name__ == '__main__':
    unittest.main()
