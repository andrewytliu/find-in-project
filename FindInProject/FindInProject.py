import gtk, gedit
import webkit
import pygtk
import os
from urllib import url2pathname
from FindInProjectParser import FindInProjectParser
from FindInProjectUtil import filebrowser_root

ui_str="""<ui>
<menubar name="MenuBar">
  <menu name="SearchMenu" action="Search">
    <placeholder name="SearchOps_0">
      <menuitem name="FindInProject" action="FindInProject"/>
    </placeholder>
  </menu>
</menubar>
</ui>
"""

style_str="""<style>
.code, .line-number {
  font-family: Consolas, Monospace,"Courier New", courier, monospace;
  word-wrap: break-word;
}
.line-number {
  width: 15px;
}
table {
  margin: 10px;
  width: 580px;
}
.filename {
  background-color: #D2D2D2;
  font-weight: bold;
}
.highlight {
  background-color: #yellow;
}
</style>"""

class FindInProjectBrowser(webkit.WebView):
    def __init__(self):
        webkit.WebView.__init__(self)

class FindInProjectWindow:
    def __init__(self):
        self._builder = gtk.Builder()
        self._builder.add_from_file(os.path.join(os.path.dirname( __file__ ), "window.glade"))
        self._window = self._builder.get_object("find-in-project")
        self._browser = FindInProjectBrowser()
        self._window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self._window.resize(600,500)
        self._window.set_destroy_with_parent(True)
        self._searchbox = self._builder.get_object("searchbox")
        self._builder.get_object("search-button").connect("clicked", self.search)
        self._builder.get_object("placeholder").add(self._browser)
        self._window.show_all()

    def init(self):
        #self._searchbox.select_region(0,-1)
        self._searchbox.grab_focus()

    def search(self, event):
        path = filebrowser_root()
        query = self._searchbox.get_active_text()
        html = FindInProjectParser(query, url2pathname(path)[7:]).html()
        self._browser.load_string(style_str + html, "text/html", "utf-8", "about:")

class FindInProjectPluginInstance:
    def __init__(self, window):
        self._window = window
        self._result = None
        self._test_file = ""
        self._test_include = ""
        self.add_menu()

    def deactivate(self):
        self._browser = None
        self.window = None
        self.plugin = None
        self.remove_menu()

    def add_menu(self):
        action_group = gtk.ActionGroup("FindInProjectActions")
        action_group.add_actions([('FindInProject', gtk.STOCK_EDIT, 'Find in project...', '<Ctrl><Shift>f', 'Search in the project', self.show_window)])
        self.manager = self._window.get_ui_manager()
        self.manager.insert_action_group(action_group, -1)
        self.manager.add_ui_from_string(ui_str)

    def remove_menu(self):
        manager = self._window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()

    def show_window(self, window):
        self._window = FindInProjectWindow()
        self._window.init()

class FindInProjectPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = FindInProjectPluginInstance(window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        pass

