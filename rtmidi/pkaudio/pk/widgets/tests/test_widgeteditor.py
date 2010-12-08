
from PyQt4.QtGui import QPixmap
from pk.gui import run_widget
from pk.gui.pov.editor.widgeteditor import WidgetEditor


class TestWidgetEditor(WidgetEditor):
    def __init__(self):
        WidgetEditor.__init__(self)
        pixmap = QPixmap('data/pk_button.png')
        assert pixmap.isNull() == False
        self.maskEditor.setPixmap(pixmap)


run_widget(TestWidgetEditor)
