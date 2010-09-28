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
.match {
  color: black;
}
tbody {
  font-family: Consolas, Monospace,"Courier New", courier, monospace;
  color: #a0a0a0;
}
table {
  margin: 10px;
  /* width: 800px; */
  border-collapse: collapse;
}
.filename {
  background-color: #D2D2D2;
  font-weight: bold;
}
.highlight {
  background-color: #yellow;
}
thead td {
  padding: 6px 10px;
}
.line-number{
  width: 43px;
  background: #D2D2D2;
  text-align:right;
  padding: 4px 6px;
}
.code{
  width: 800px;
  word-wrap: break-word;
  display: block;
}
tbody tr:nth-child(even) td:nth-child(2){
  background: #efefef;
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
        self._window.set_title("Find in Project")
        self._window.connect("delete_event", self._window.hide_on_delete)
        self._window.connect("key-release-event", self.window_key)
        self._searchbox = self._builder.get_object("searchbox")
        self._searchbox.connect("key-release-event", self.searchbox_key)
        self._builder.get_object("search-button").connect("clicked", self.search)
        self._builder.get_object("placeholder").add(self._browser)

    def init(self):
        #self._searchbox.select_region(0,-1)
        self._window.show_all()
        self._searchbox.grab_focus()

    def window_key(self, widget, event):
        if event.keyval == gtk.keysyms.Escape:
            self._window.hide()

    def searchbox_key(self, widget, event):
        if event.keyval == gtk.keysyms.Return:
            self._builder.get_object("search-button").grab_focus()
            self.search(event)

    def search(self, event):
        path = filebrowser_root()
        query = self._searchbox.get_active_text()
        html = FindInProjectParser(query, url2pathname(path)[7:]).html()
        self._browser.load_string(style_str + html, "text/html", "utf-8", "about:")
        print style_str + html

class FindInProjectPluginInstance:
    def __init__(self, window):
        self._window = window
        self._search_window = FindInProjectWindow()
        self.add_menu()

    def deactivate(self):
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
        self._search_window.init()

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

