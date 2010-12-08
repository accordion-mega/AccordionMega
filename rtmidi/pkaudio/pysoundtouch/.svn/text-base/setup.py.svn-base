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


import os
from distutils.core import setup, Extension

sources = ['AAFilter.cpp',
           'FIFOSampleBuffer.cpp',
           'FIRFilter.cpp',
           'RateTransposer.cpp',
           'SoundTouch.cpp',
           'TDStretch.cpp',
           'BPMDetect.cpp',
           'PeakFinder.cpp',
           ]

sources_gcc = ['cpu_detect_x86_gcc.cpp',
               'mmx_gcc.cpp',
               ]

sources_win = ['cpu_detect_x86_win.cpp',
               'mmx_win.cpp',
               '3dnow_win.cpp',
               'sse_win.cpp',
               ]

if hasattr(os, 'uname'):
    sources += sources_gcc
else:
    sources += sources_win
libSoundTouch_sources = [os.path.join('libsoundtouch', i) for i in sources]

soundtouch = Extension('soundtouch',
                       sources=['soundtouchmodule.cpp',
                                ] + libSoundTouch_sources,
                       extra_compile_args=['-fcheck-new', '-O3'],
                       )


setup(name = 'soundtouch',
      version = '0.1',
      description = 'Python libSoundTouch interface',
      ext_modules = [soundtouch])

