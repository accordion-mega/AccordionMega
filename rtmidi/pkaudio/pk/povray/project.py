"""
Functions for manipulating directories and files in a project.
"""

import os, os.path
from elementtree import ElementTree
import utils

#import templates
#from packageeditor import PackageEditor
#from projectform import Ui_ProjectForm


class Project:
    """ Project data """
    def __init__(self):
        self.widgets = []

    def _entry(self):
        return { 'name' : '',
                 'frames' : 0,
                 'x' : 0,
                 'y' : 0,
                 'w' : 0,
                 'h' : 0,
                 }

    def write(self, fpath):
        """ write the project data to a file. """
        root = ElementTree.Element('xml')
        for entry in self.widgets:
            elem = ElementTree.SubElement(root, 'widget')
            elem.attrib['name'] = entry['name']
            elem.attrib['frames'] = str(entry['frames'])
            elem.attrib['x'] = str(entry['x'])
            elem.attrib['y'] = str(entry['y'])
            elem.attrib['w'] = str(entry['w'])
            elem.attrib['h'] = str(entry['h'])
        ElementTree.ElementTree(root).write(fpath)
    
    def read(self, fpath):
        """ load the project data from a file. """
        for elem in ElementTree.parse(fpath).getroot():
            if elem.tag == 'widget':
                entry = self._entry()
                entry['name'] = elem.attrib['name']
                entry['frames'] = int(elem.attrib['frames'])
                entry['x'] = int(elem.attrib['x'])
                entry['y'] = int(elem.attrib['y'])
                entry['w'] = int(elem.attrib['w'])
                entry['h'] = int(elem.attrib['h'])
                self.widgets.append(entry)

    def get_widgets(self):
        return [m['name'] for m in self.widgets]

    def set_widget(self, name, frames=None, mask=None):
        widget = None
        for entry in self.widgets:
            if entry['name'] == name:
                widget = entry
                self.widgets.remove(entry)
                break
        if not widget:
            widget = self._entry()
            widget['name'] = name
        if not frames is None:
            widget['frames'] = frames
        if not mask is None:
            widget['x'] = mask[0]
            widget['y'] = mask[1]
            widget['w'] = mask[2]
            widget['h'] = mask[3]
        self.widgets.append(widget)

    def del_widget(self, name):
        self.widgets = [entry for entry in self.widgets
                        if entry['name'] != name]

    def get_widget(self, name):
        for entry in self.widgets:
            if entry['name'] == name:
                return entry

    def import_dir(self, path):
        """ import existing directory, using blank masks. """
        self.widgets = []
        for name in utils.get_modules(path):
            self.set_widget(name)

    def rename_widget(self, old, new):
        """ Change the name of a widget. """
        widget = self.get_widget(old)
        self.remove_widget(old)
        widget['name'] = new
        self.set_widget(new, frames=widget['frames'],
                        x=widget['x'], y=widget['y'],
                        w=widget['w'], h=widget['h'])




def create_project(path, name, author, email, version):
    """ Create a project directory, etc. Overwrite if necessary. """
    if not os.path.isdir(path):
        os.makedirs(path)
    name = name + '.pkpov'
    xml = pk.xml.XML(schema=utils.PovSchema)
    fpath = os.path.join(path, name)
    xml.writeFile(fpath)

    inc_path = os.path.join(path, utils.MAIN_INC+'.inc')
    open(inc_path, 'w').write(templates.MAIN_INC)
    return fpath


def setup_widget_dir(path, name):
    """ Create a directory and pov files for a widget. """
    mpath = os.path.join(path, name)
    os.mkdir(mpath)
    

    capName = pk.utils.cap_name(name)
    include = utils.MAIN_INC

    inc_text = templates.render_inc(name, 'pkpov')
    pov_text = templates.render_pov(name, name,
                                    'ButtonIndentShape',
                                    'ButtonClockedColor')

    inc_path = os.path.join(path, name+'.inc')
    pov_path = os.path.join(path, name, name+'.pov')

    open(inc_path, 'w').write(inc_text)
    open(pov_path, 'w').write(pov_text)

    
def rename_widget(path, old_name, new_name):
    """ rename the directory and repective files.
    how about a sed replace for names here?
    """
    old_path = os.path.join(path, old_name)
    new_path = os.path.join(path, new_name)
    
    print 'renaming %s to %s' % (old_path, new_path)
    os.rename(old_path, new_path)
    
    old_inc_path = os.path.join(path, old_name+'.inc')
    new_inc_path = os.path.join(path, new_name+'.inc')
    print 'renaming %s to %s' % (old_inc_path, new_inc_path)
    os.rename(old_inc_path, new_inc_path)
    
    old_pov_path = os.path.join(new_path, old_name+'.pov')
    new_pov_path = os.path.join(new_path, new_name+'.pov')
    os.rename(old_pov_path, new_pov_path)
