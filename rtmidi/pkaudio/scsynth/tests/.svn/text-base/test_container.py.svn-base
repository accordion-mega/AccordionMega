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
from scsynth import container


class ContainerProxyBaseTest(unittest.TestCase):
    
    def test_unique(self):
        proxy1 = container.ContainerProxyBase(data=[1, 2, 3])
        self.assertEqual(len(proxy1), 3)
        
        proxy2 = container.ContainerProxyBase(data=[4, 5, 6])
        self.assertEqual(len(proxy2), 3)

    def test_attr(self):
        proxy = container.ContainerProxyBase([])
        
        proxy.x = 1
        self.assertEqual(proxy.x, 1)
        
        proxy.x = 2
        self.assertEqual(proxy.x, 2)


class ListProxyTest(unittest.TestCase):

    def test_append(self):
        proxy = container.ListProxy()

        proxy.append(-1)
        self.assertEqual(len(proxy), 1)
        self.assertEqual(proxy[0], -1)

        proxy.append(-2)
        self.assertEqual(len(proxy), 2)
        self.assertEqual(proxy[1], -2)

    def test_iter(self):
        proxy = container.ListProxy()
        input = [1, 2, 3]
        for i in input:
            proxy.append(i)
        output = [].extend(proxy)
        self.assertEqual(input, [1,2,3])


if __name__ == '__main__':
    unittest.main()
