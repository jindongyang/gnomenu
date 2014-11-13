#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!
#
#(c) Whise 2010 <helderfraga@gmail.com>

# Dbus GnoMenu interface, and dockmanager (docky) script, it "tricks" docky


import atexit
import gconf
import gobject
import glib
import sys
import urllib
import os

try:
	from dockmanager.dockmanager import DockManagerItem, DockManagerSink, DOCKITEM_IFACE
	from signal import signal, SIGTERM
	from sys import exit
except ImportError, e:
	print e
	exit()
	
import dbus
import dbus.service
import dbus.mainloop.glib
import gtk

gconf_client = gconf.client_get_default()
try:
	INSTALL_PREFIX = open("/etc/gnomenu/prefix").read()[:-1] 
except:
	INSTALL_PREFIX = '/usr'
sys.path.append(INSTALL_PREFIX + '/lib/gnomenu')
import backend
import gettext
gettext.textdomain('gnomenu')
gettext.install('gnomenu', INSTALL_PREFIX +  '/share/locale')
gettext.bindtextdomain('gnomenu', INSTALL_PREFIX +  '/share/locale')


orient = gconf_client.get_string("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/Position")
size = gconf_client.get_int("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/IconSize")
if gconf_client.get_bool("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/ZoomEnabled"):
	per =  gconf_client.get_float("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/ZoomPercent")
else: per = 1
per = 1
lista = gconf_client.get_list("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/SortList",1)
if INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop' in lista:
	pos = lista.index(INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop')
else: 
	lista.append(INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop')
	gconf_client.set_list("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/SortList",1,lista)
	pos = len(lista)


lista1 = gconf_client.get_list("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/Launchers",1)
if not 'file://' + INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop' in lista1:
	lista1.append('file://' + INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop')
	gconf_client.set_list("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/Launchers",1,lista1)
	# Set the launcher in docky
	

position = gtk.gdk.get_default_root_window().get_pointer()[0]

#gtk.gdk.screen_width()/2 - (len(lista)*size)/2 + (pos * size)+ size #last size is for the anchor
print position

if orient == "Top":
	backend.save_setting('orientation', 'top')
else:
	backend.save_setting('orientation', 'bottom')


class TestObject(dbus.service.Object):
    def __init__(self, conn, object_path='/com/gnomenu/GnoMenu/object'):
        dbus.service.Object.__init__(self, conn, object_path)
	from Menu_Main import Main_Menu
	self.Main_Menu = Main_Menu
	import Globals as Globals
	self.Globals = Globals
	self.hwg = self.Main_Menu(self.HideMenu)

    @dbus.service.signal('com.gnomenu.GnoMenu')
    def Activate(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
	if orient == "Top":
		self.hwg.Adjust_Window_Dimensions(int(gtk.gdk.get_default_root_window().get_pointer()[0]- (self.Globals.MenuWidth/2)),int(size*per))
	else:
		self.hwg.Adjust_Window_Dimensions(int(gtk.gdk.get_default_root_window().get_pointer()[0]- (self.Globals.MenuWidth/2)),int(gtk.gdk.screen_height()-self.Globals.MenuHeight-size*per))
	if not self.hwg.window.window:
		self.hwg.show_window()
	else:
		if not self.hwg.window.window.is_visible():
			self.hwg.show_window()
		else: self.HideMenu()


    @dbus.service.method('com.gnomenu.GnoMenu')
    def emitActivate(self):
        #you emit signals by calling the signal's skeleton method
        self.Activate('Hello')
        return 'Signal emitted'

    @dbus.service.method("com.gnomenu.GnoMenu",
                         in_signature='', out_signature='')
    def Exit(self):
	#import utils
	#utils.show_message('aaaaaa')
        loop.quit()

    def HideMenu(self):
	if self.hwg:
		if self.hwg.window.window:
			if self.hwg.window.window.is_visible()== True:
				self.hwg.hide_window()

class DockyGnoMenuItem(DockManagerItem):
	def __init__(self, sink, path):
		DockManagerItem.__init__(self, sink, path)
		import Globals as Globals
		self.Globals = Globals
		import utils
		self.utils = utils
		if self.Globals.Settings['Distributor_Logo']:
			import IconFactory as iconfactory
			self.iconfactory = iconfactory
			self.set_icon(self.iconfactory.GetSystemIcon('distributor-logo'))
		else: self.set_icon(self.Globals.Applogo)
		self.add_menu_item(_("Preferences"),gtk.STOCK_PREFERENCES)
		self.add_menu_item( _("About"),gtk.STOCK_ABOUT)
		self.add_menu_item( _("Edit Menus"),gtk.STOCK_EDIT)



	def properties(self,event=0,data=None):
		#os.spawnvp(os.P_WAIT,Globals.ProgramDirectory+"GnoMenu-Settings.py",[Globals.ProgramDirectory+"GnoMenu-Settings.py"])
		os.system("/bin/sh -c '"+self.Globals.ProgramDirectory+"GnoMenu-Settings.py' &")
		# Fixme, reload stuff properly
		
		
	def about_info(self,event=0,data=None):
		os.system("/bin/sh -c " + INSTALL_PREFIX +"'/lib/"+self.Globals.appdirname+"/GnoMenu-Settings.py --about' &")

	def edit_menus(self,event=0, data=None):
		os.system("alacarte &")
		#ConstructMainMenu()



	def menu_pressed(self, menu_id):
		#self.utils.show_message(self.id_map)
		if self.id_map[menu_id] == _("Preferences"):
			self.properties()
		elif self.id_map[menu_id] == _('About'):
			self.about_info()
		elif self.id_map[menu_id] == _("Edit Menus"):
			self.edit_menus()
		
		


class DockyGnoMenuSink(DockManagerSink):
	def item_path_found(self, pathtoitem, item):
		if item.Get(DOCKITEM_IFACE, "Uri", dbus_interface="org.freedesktop.DBus.Properties").startswith ("file://"):
			self.items[pathtoitem] = DockyGnoMenuItem(self, pathtoitem)

GnoMenusink = DockyGnoMenuSink()

def cleanup ():
	lista.remove(INSTALL_PREFIX + '/share/dockmanager/scripts/GnoMenu/GnoMenuDocky.desktop')
	gconf_client.set_list("/apps/docky-2/Docky/Interface/DockPreferences/Dock1/SortList",1,lista)
	GnoMenusink.dispose ()
	sys.exit()

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    atexit.register (cleanup)
    signal(SIGTERM, lambda signum, stack_frame: exit(1))
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName('com.gnomenu.GnoMenu', session_bus)
    loop = gobject.MainLoop()
    object = TestObject(session_bus)
    loop.run()
