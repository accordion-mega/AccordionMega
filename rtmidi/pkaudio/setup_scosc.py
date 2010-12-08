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


packages = ['scosc',
            'scsynth',
            ]
scripts = ['bin/pkechoosc',
           ]

if __name__ == '__main__':
    from distutils.core import Extension, setup
    setup(name="scosc",
          version="0.1",
          description="scsynth communication",
          author_email="patrickkidd@gmail.com",
          url="http://www.patrickkidd.com",
          packages=packages,
          scripts=scripts,
          )
