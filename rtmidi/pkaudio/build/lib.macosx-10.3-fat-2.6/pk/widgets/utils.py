"""
Graphical User Interface functions. This package requires PyQt4.
"""

import os
import sys
from PyQt4.QtGui import QColor, QSpacerItem, QHBoxLayout, QLayout


POV_COLOR = QColor(136, 136, 136)


def h_centered(layout, item):
    l_spacer = QSpacerItem(0, 0)
    r_spacer = QSpacerItem(0, 0)
    proxy = QHBoxLayout()
    proxy.setSpacing(0)
    proxy.setMargin(0)
    proxy.addItem(l_spacer)
    if isinstance(item, QLayout):
        proxy.addLayout(item)
    else:
        proxy.addWidget(item)
    proxy.addItem(r_spacer)
    layout.addLayout(proxy)



def run_widget(myclass):
    """ run a qt app using myclass as the main widget.
    This funtion calls sys.exit().
    """
    from PyQt4.QtGui import QApplication
    a = QApplication(sys.argv)
    a.setStartDragDistance(8)
    w = myclass()
    w.show()
    sys.exit(a.exec_())
