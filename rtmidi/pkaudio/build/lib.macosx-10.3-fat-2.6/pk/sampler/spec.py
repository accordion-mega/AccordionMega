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
constants
"""

import os.path
from PyQt4.QtGui import QColor, QFrame
from pk.widgets.utils import POV_COLOR

SCROLLPAD_WIDTH = 40
SCROLLPAD_COLOR = QColor(255, 255, 0, 200)
FRAME_SHAPE = QFrame.WinPanel
BACKGROUND = POV_COLOR.light(125)
PART_WIDTH = 100
PART_HEIGHT = 55

PKSAMPLER = os.path.join(os.environ['HOME'], '.pksampler')
LOOPS = os.path.join(PKSAMPLER, 'loops')
PATTERNS = os.path.join(PKSAMPLER, 'patterns')

