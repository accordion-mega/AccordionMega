#!/bin/env python
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

"""
Unit test for uguru module.
This only runs on an A-Bit uguru motherboard.
"""

import unittest
import uguru


class Test_uGuru(unittest.TestCase):
    def test_one(self):
        self.assertRaises(uguru.error, uguru.read_sensor, -1)
        self.assertRaises(uguru.error, uguru.read_sensor, 20)
        
    def test_read(self):
        uguru.read_sensor(uguru.SENS_CPUTEMP)
        uguru.read_sensor(uguru.SENS_SYSTEMP)
        uguru.read_sensor(uguru.SENS_PWMTEMP)
        uguru.read_sensor(uguru.SENS_VCORE)
        uguru.read_sensor(uguru.SENS_DDRVDD)
        uguru.read_sensor(uguru.SENS_DDRVTT)
        uguru.read_sensor(uguru.SENS_NBVDD)
        uguru.read_sensor(uguru.SENS_SBVDD)
        uguru.read_sensor(uguru.SENS_HTV)
        uguru.read_sensor(uguru.SENS_AGP)
        uguru.read_sensor(uguru.SENS_5V)
        uguru.read_sensor(uguru.SENS_3V3)
        uguru.read_sensor(uguru.SENS_5VSB)
        uguru.read_sensor(uguru.SENS_3VDUAL)
        uguru.read_sensor(uguru.SENS_CPUFAN)
        uguru.read_sensor(uguru.SENS_NBFAN)
        uguru.read_sensor(uguru.SENS_SYSFAN)
        uguru.read_sensor(uguru.SENS_AUXFAN1)
        uguru.read_sensor(uguru.SENS_AUXFAN2)


if __name__ == '__main__':
    unittest.main()
    
