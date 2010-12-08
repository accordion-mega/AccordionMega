import os, os.path
from pk.widgets import run_widget
from pk.widgets import TextEditor, TabbedEditor


PATH = os.path.join(os.getcwd(), 'data/project.pk')

def Test():
    edit = TextEditor(mime='text/x-c++src')
    edit.openURL(PATH)
    return edit


class TestTabEditor(TabbedEditor):
    def __init__(self):
        TabbedEditor.__init__(self)
        HOME = os.environ['HOME']
        self.addEditor(os.path.join(HOME, '.bash_profile'),
                       'text/x-c++src')
        self.addEditor('/etc/profile',
                       'text/x-c++src')
        self.resize(500,500)


run_widget(Test)
