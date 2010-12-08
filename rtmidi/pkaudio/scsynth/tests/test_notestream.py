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


def read(stream, steps):
    ret = []
    for i in range(steps):
        ret.extend(stream.read())
    return ret


class NoteStreamTest(unittest.TestCase):

    def setUp(self):
        self.pattern = scsynth.Pattern()
        for i in (192, 0, 128, 64):
            self.pattern.add(scsynth.Note(i, i+1, 64))
        self.stream = scsynth.NoteStream(self.pattern)

    def test_noloop(self):
        self.stream.loop(False)

        notes = read(self.stream, 64)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].start, 0)

        notes = read(self.stream, 65)
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].start, 64)
        self.assertEqual(notes[1].start, 128)
        
        notes = read(self.stream, 256)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].start, 192)

        notes = read(self.stream, 256)
        self.assertEqual(len(notes), 0)

    def test_loop(self):
        self.stream.loop(True)
        
        notes = read(self.stream, 1000)
        self.assertEqual(len(notes), 1000 / 64 + 1)

        prev = notes[0]
        for note in notes[1:]:
            self.assertEqual(note.start - prev.start, 64)
            prev = note

    def _test_sparse_noloop(self):
        patt = sequencer.Pattern()
        patt.beats = 16
        for i in (192, 0, 128, 1024, 64):
            patt.add(sequencer.Note(i, i+1, 64))
        stream = sequencer.NoteStream(patt)
        stream.loop(False)

        notes = read(self.stream, 256)
        self.assertEqual(len(notes), 4)

        notes = read(self.stream, 2000)
        self.assertEqual(len(notes), 32)
        self.assertEqual(notes[4].start, 1024)

        notes = read(self.stream, 10000)
        self.assertEqual(len(notes), 5)
        self.assertEqual(notes[4].start, 1024)


if __name__ == '__main__':
    unittest.main()
