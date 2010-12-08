"""
A column o tabbed widget items
"""


from PyQt4.QtGui import QToolBox

class ToolBox(QToolBox):
    def __init__(self, parent=None):
        QToolBox.__init__(self, parent)

