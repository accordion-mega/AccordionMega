
from PyQt4.QtGui import QPixmap
import pk.widgets.utils
from pk.widgets.maskeditor import MaskEditor

PNG = 'data/pk_button.png'

class TestMaskEditor(MaskEditor):
    def __init__(self):
        MaskEditor.__init__(self)
        pixmap = QPixmap(PNG)
        assert pixmap.isNull() == False
        self.setPixmap(pixmap)
        self.resize(200,200)

pk.widgets.utils.run_widget(TestMaskEditor)

