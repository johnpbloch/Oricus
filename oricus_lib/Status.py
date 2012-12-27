from gi.repository import GObject

class StatusBar():
    statusbar = None
    
    def __init__(self, statusbar):
        self.statusbar = statusbar
        
    def set(self, message, context=None):
        if context is None:
            context = Types.DEFAULT
        self.statusbar.push(context, message)

    def clear(self, context=None, Delay=None):
        if context is None:
            context = Types.DEFAULT
        if Delay is None:
            self.statusbar.pop(context)
            return False
        try:
            GObject.timeout_add(Delay, self.clear, context)
        except:
            pass
        
class Types():
    (DEFAULT,
     STARTUP,
     TOGGLE) = range(1, 4)
