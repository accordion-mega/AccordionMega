"""
Text editor widgets and functions.
"""


from PyQt4.QtGui import QWidget, QSizePolicy, QTextEdit, QTabWidget, QFont
from PyQt4.QtGui import QVBoxLayout, QFontMetrics
import utils



class KPartTextEditor(QWidget):
    def __init__(self, mime, parent=None):
        QWidget.__init__(self, parent)
        Layout = QVBoxLayout(self)
        self.part = partchooser.get_part(self, mime)
        if self.part is None:
            return
        self.part.widget().setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        Layout.addWidget(self.part.widget())
        self.fpath = None

    def openURL(self, url):
        from kdecore import KURL
        self.url = KURL(url)
        if self.part:
            self.part.openURL(self.url)

    def filename(self):
        return str(self.url.fileName())

    def save(self, fpath=None):
        if fpath is None and self.fpath is None:
            pass

    def clear(self):
        self.openUrl('/dev/null')


class QtTextEditor(QTextEdit):
    def __init__(self, mime, parent=None):
        QTextEdit.__init__(self, parent)
        self.setAcceptRichText(False)
        font = QFont()
        font.setFamily('Terminal [DEC]')
        self.setFont(font)
        ts = QFontMetrics(font).maxWidth()

    def openURL(self, url):
        f = open(url, 'r')
        self.setPlainText(f.read())
        self.fpath = url

    def filename(self):
        return self.fpath

    def save(self, fpath=None):
        if fpath is None and self.fpath is None:
            pass
        f = open(self.fpath, 'w')
        f.write(str(self.toPlainText()))

    def clear(self):
        self.setText('')


def TextEditor(mime, parent=None):
    if utils.has_kde():
        return KPartTextEditor(mime, parent)
    else:
        return QtTextEditor(mime, parent)

 
class TabbedEditor(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.editors = []
        
    def addEditor(self, url, mime, index=-1):
        if index == -1:
            editor = Editor(mime)
            editor.openURL(url)
            self.insertTab(editor, editor.filename(), False)


