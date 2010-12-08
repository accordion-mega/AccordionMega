
class error(Exception):
    pass


class GstError(error):
    def __init__(self, msg):
        error.__init__(self, '[GStreamer Error] %s' % msg)


import sys
import time
import gst
import gobject
from PyQt4.QtCore import QObject, QEvent, QTimer, SIGNAL, QThread, QEventLoop
from PyQt4.QtGui import QApplication


gobject.threads_init()

class QMainLoopSrc(gobject.Source):
    """ A GSource to add to a mainloop. Use in place of a QApplication
    or gobject.MainLoop. This shoud be optimized in check and prepare
    to be usable.
    """
    def __init__(self, args=sys.argv):
        gobject.Source.__init__(self)
        self.qapp = QApplication(args)
        
        self.loop = gobject.MainLoop()
        self.attach(self.loop.get_context())
        
        self.run = self.loop.run

    def quit(self):
        self.qapp.quit()
        self.loop.quit()

    def prepare(self):
        """ """
        # ugg just keep checking
        return (-1, True)
    
    def check(self):
        """ maybe add an idle call via QTimer.start(0) just before the
        event to see if it is idle, the return False?
        """
        return True
    
    def dispatch(self, *args):
        try:
            self.qapp.processEvents(QEventLoop.AllEvents)
        except KeyboardInterrupt, e:
            pass
        return True


class GObjectLoop:
    """ Manages a gobject.MainLoop, the inverse of QMainLoop. """

    _instance = None

    def __init__(self):
        if not GObjectLoop._instance is None:
            raise RuntimeError('there can only be one GObjectLoop')
        else:
            GObjectLoop._instance = self
        self.gmainloop = gobject.MainLoop()
        # this is horribly inefficient!
        self.gcontext = self.gmainloop.get_context()
        self.idletimer = QTimer(QApplication.instance())
        QObject.connect(self.idletimer, SIGNAL('timeout()'),
                        self.on_idle)
        self.idletimer.start(0)
        
    def __del__(self):
        self.gmainloop.quit()
        
    def on_idle(self):
        while self.gcontext.pending():
            self.gcontext.iteration()

# this prevents a seg fault, not sure why.
import atexit
def _atexit():
    if GObjectLoop:
        GObjectLoop._instance = None
atexit.register(_atexit)


_last_qevent_type = QEvent.User
def qevent_user():
    global _last_qevent_type
    _last_qevent_type += 1
    return QEvent.Type(_last_qevent_type)

EVENT_UNKNOWN = qevent_user()
EVENT_NEW_CLOCK = qevent_user()
EVENT_CLOCK_PROVIDE = qevent_user()
EVENT_MESSAGE_TAG = qevent_user()
EVENT_MESSAGE_STATE_CHANGED = qevent_user()
EVENT_MESSAGE_ERROR = qevent_user()


class GstEvent(QEvent):
    def __init__(self, msg):
        QEvent.__init__(self, QEvent.User)
        self.msg = msg
        self.src = msg.src
        self._type = msg.type
        
    def type(self):
        return self._type


class QGstObject(QObject):
    """ Converts gst events to QEvent objects. """

    def __init__(self, gelement, parent=None):
        QObject.__init__(self, parent)
        self._gelement = gelement
        self._gelement.get_bus().add_signal_watch()
        self._gelement.get_bus().connect('message', self.cb_bus)
        if GObjectLoop._instance is None:
            GObjectLoop()

    def cb_bus(self, bus, msg):
        """ Attempt to translate a GstMessage and appropriate data to
        a QEvent.
        """
        QApplication.instance().sendEvent(self, GstEvent(msg))

    def event(self, e):
        if isinstance(e, GstEvent):
            return self.gstEvent(e)
        else:
            return QObject.event(self, e)

    def gstEvent(self, e):
        """ Reimplement this to catch GstEvents. """
        return True

    def change_state(self, target_state):
        status = self._gelement.set_state(target_state)
        if status == gst.STATE_CHANGE_FAILURE:
            raise GstError('failure setting state to %s' % target_state)
        status, old, new = self._gelement.get_state(target_state)

#    def handle_gst_event(self, bus, msg):
#        mtype = msg.type
#        if mtype == gst.MESSAGE_CLOCK_PROVIDE:
#            clock, ready = msg.parse_clock_provide()
#            qapp.postEvent(self, GstEvent(EVENT_NEW_CLOCK, msg))
#            
#        elif mtype == gst.MESSAGE_NEW_CLOCK:
#            clock = msg.parse_new_clock()
#            qevent = GstEvent(EVENT_NEW_CLOCK, msg)
#            qevent.clock = clock
#            qapp.postEvent(self, qevent)
#            
#        elif mtype == gst.MESSAGE_TAG:
#            taglist = msg.parse_tag()
#            qevent = GstEvent(EVENT_MESSAGE_TAG, msg)
#            qevent.taglist = []
#            for k in taglist.keys():
#                 qevent.taglist[k] = taglist[k]
#            qapp.postEvent(self, qevent)
#            
#        elif mtype == gst.MESSAGE_STATE_CHANGED:
#            old, new, pending = msg.parse_state_changed()
#            # ignore events for bin elements, we only want ones for the bin.
#            if msg.src == self._gelement:
#                qevent = GstEvent(EVENT_MESSAGE_STATE_CHANGED, msg)
#                qevent.src = msg.src
#                qevent.old = old
#                qevent.new = new
#                qevent.pending = pending
#                qapp.postEvent(self, qevent)
#                
#        elif mtype == gst.MESSAGE_ERROR:
#            gerror, debug = msg.parse_error()
#            qevent = GstEvent(EVENT_MESSAGE_ERROR, msg)
#            qevent.gerror = gerror
#            qevent.debug = debug
#            qapp.postEvent(self, qevent)
#            
#        else:
#            qapp.postEvent(self, GstEvent(EVENT_UNKNOWN, msg))

