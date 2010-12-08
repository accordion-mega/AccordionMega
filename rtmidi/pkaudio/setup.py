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
"""
Setup script for the pk package and scripts.
"""

import sys
from distutils.core import setup

import setup_rtmidi
import setup_pk
import setup_scosc

ext_modules = []
ext_modules += setup_rtmidi.ext_modules

packages = []
packages += setup_pk.packages
packages += setup_scosc.packages

scripts = []
scripts += setup_pk.scripts
scripts += setup_pk.scripts

setup(name="pksampler",
      version="0.4b",
      description="The pksampler",
      author_email="patrickkidd@gmail.com",
      url="http://pksampler.sourceforge.net",
      packages=packages,
      scripts=scripts,
      ext_modules=ext_modules,
      )

