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

if hasattr(os, 'uname'):
    OSNAME = os.uname()[0]
else:
    OSNAME = 'Windows'

define_macros = []
libraries = []
extra_link_args = []

sources=['rtmidimodule.cpp',
         'RtMidi.cpp',
         ]

if OSNAME == 'Linux':
    define_macros=[("__LINUX_ALSASEQ__", '')]
    libraries = ['asound', 'pthread']

elif OSNAME == 'Darwin':
    define_macros = [('__MACOSX_CORE__', '')]
    libraries = ['pthread']
    extra_link_args = ['-framework', 'CoreAudio',
                       '-framework', 'CoreMidi',
                       '-framework', 'CoreFoundation']

elif OSNAME == 'Windows':
    define_macros = [('__WINDOWS_MM__', '')]
    libraries = ['winmm.lib', 'multithreaded']

elif OSNAME == 'Irix':
    define_macros = [('__IRIX_MD__', '')]
    libraries = ['pthread', 'md']

sources = [os.path.join('pyrtmidi', sfile) for sfile in sources]
RtMidi = Extension('rtmidi',
                   sources=sources,
                   libraries=libraries,
                   define_macros=define_macros,
                   extra_link_args = extra_link_args,
                   )

ext_modules = [RtMidi]
if __name__ == '__main__':
    setup(name='rtmidi',
          version='0.1',
          description='Python RtMidi interface',
          ext_modules=ext_modules)

