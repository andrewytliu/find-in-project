from gi.repository import GObject, Peas, Gedit
from FindInProject import FindInProjectPluginInstance

class FindInProjectPlugin(GObject.Object, Gedit.WindowActivate):
    __gtype_name__ = "FindInProjectPlugin"  

    window = GObject.property(type=Gedit.Window)
  
    def __init__(self):
        GObject.Object.__init__(self)
        self._instances = {}

    def activate(self):
        self._instances[self.window] = FindInProjectPluginInstance(window)

    def deactivate(self):
        self._instances[self.window].deactivate()
        del self._instances[self.window]

    def update_ui(self):
        pass

