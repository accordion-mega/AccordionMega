

class PartException(ValueError):
    pass


offer_cache = {}
def get_offer_list(mime):
    """ Cache and return an offer list. """
    from kio import KTrader
    global offer_cache
    ret = []
    if mime in offer_cache:
        return offer_cache[mime]
    else:
        t = KTrader.self()
        offers = t.query(mime, "")
        s = None
        if offers:
            ret = []
            for o in offers:
                lib = str(o.library())
                if lib:
                    ret.append(o)
            offer_cache[mime] = ret
        return ret
        

def get_part(parent, mime):
    """ Return the preferred cpp editor part. """
    import kparts
    try:
        partname = pk.conf.get(CONF, mime+'_PART')
    except pk.conf.InvalidKey:
        choosePart(mime)
        try:
            partname = pk.conf.get(CONF, mime+'_PART')
        except pk.conf.InvalidKey:
            return
    ret = None
    for o in get_offer_list(mime):
        name = str(o.name())
        if name == partname:
            ret = kparts.createReadWritePart(o.library(), 
                                             parent, 
                                             o.name())
    if ret:
        return ret
    else:
        raise PartException('no parts for mime \"%s\" available' % mime)


from partchooserform import Ui_PartChooserForm
class PartChooserDialog(Ui_PartChooserForm):
    """ Chooses a part for a mime type. """
    def __init__(self, mime, parent=None, name='', modal=False, f=0):
        partchooserform.__init__(self, parent, name, modal, f)
        self.mime = mime
        for o in get_offer_list(self.mime):
            self.comboBox.insertItem(o.name())
    
    def accept(self):
        val = str(self.comboBox.currentText())
        if val:
            pk.conf.set(CONF, self.mime+'_PART', val)
        partchooserform.accept(self)
        
    def exec_loop(self):
        """ Change the value to match the stored value. """
        try:
            val = pk.conf.get(CONF, self.mime+'_PART')
            for i in range(self.comboBox.count()):
                if val == str(self.comboBox.text(i)):
                    self.comboBox.setCurrentItem(i)
                    break
        except pk.conf.InvalidKey:
            pass
        partchooserform.exec_loop(self)
        

    
def choosePart(mime):
    """ Pop a dialog to choose an editor part. 
    """
    dlg = PartChooserDialog(mime, None, "PartChooser", True)
    return dlg.exec_loop()
