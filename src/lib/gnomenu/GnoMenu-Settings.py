#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!
#
#(c) Whise 2009,2010 <helderfraga@gmail.com>

# Gnomenu settings manager
# Part of the GnoMenu


import pygtk
pygtk.require('2.0')
import gtk
import os
import commands
import sys
import pango
import Globals
if len(sys.argv) == 2 and sys.argv[1] == "--welcome":
	Globals.FirstUse = True
import xml.dom.minidom
import utils
import backend
import IconFactory
try:
	import tarfile as tarfile
	hastar = True
except:
	hastar = False
import urllib

try:
	INSTALL_PREFIX = open("/etc/gnomenu/prefix").read()[:-1] 
except:
	INSTALL_PREFIX = '/usr'

import gettext

gettext.textdomain('gnomenu')
gettext.install('gnomenu', INSTALL_PREFIX +  '/share/locale')
gettext.bindtextdomain('gnomenu', INSTALL_PREFIX +  '/share/locale')

def _(s):
	return gettext.gettext(s)


class GnoMenuSettings:


	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title(_('GnoMenu About'))
		self.window.set_default_size(300,180)
		self.window.set_icon(gtk.gdk.pixbuf_new_from_file(Globals.Applogo))
		self.window.set_border_width(4)
		self.vbox = gtk.VBox()
		self.window.add(self.vbox)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.hbox1 = gtk.HBox()
		self.vbox.pack_end(self.hbox1, False, False)
		self.button1 = gtk.Button(_('Close'))
		self.button1.set_size_request(50,30)
		self.button1.connect("clicked", self.buttonpress,'ok')
		self.hbox1.pack_end(self.button1, True, True)

		self.vbox_about = gtk.VBox()
		self.image_logo = gtk.Image()
		self.image_logo.set_size_request(80,80)
		self.Applogo = gtk.gdk.pixbuf_new_from_file_at_size(Globals.Applogo,80,80)
		self.image_logo.set_from_pixbuf(self.Applogo)
		self.label_app = gtk.Label(_("GnoMenu %s") % Globals.version)
		self.label_credits = gtk.Label(_("Consolidated menu for the GNOME desktop.\n"))
		self.font_desc = pango.FontDescription('sans bold 14')
		self.label_app.modify_font(self.font_desc)
		self.label_credits.set_justify(gtk.JUSTIFY_CENTER)
		self.vbox_about.pack_start(self.image_logo, False, False)
		self.vbox_about.pack_start(self.label_app, False, False,10)
		self.vbox_about.pack_start(self.label_credits, False, False,10)

		self.vbox.pack_end(self.vbox_about, False, False)
		self.window.show_all()

	def buttonpress(self,widget,id):
		if id == 'ok':
			gtk.main_quit()
	
def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	GnoMenuSettings()
	main()

