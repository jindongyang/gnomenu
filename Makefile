# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!
#
#(c) QB89Dragon 2007/8 <hughescih@hotmail.com>
#(c) Whise 2009 <helderfraga@gmail.com>
#
# A simple makefile to allow installing/uninstalling 
# Part of the GnoMenu

PREFIX = /usr
AWNPREFIX = $(PREFIX)
CAIRODOCKPREFIX = $(PREFIX)
DOCKYPREFIX = $(PREFIX)
INSTALL_LOG = install.log
LIBDIR = $(PREFIX)/lib

.PHONY : install
.PHONY : uninstall

all:
	@echo "Makefile: Available actions: install, uninstall,"
	@echo "Makefile: Available variables: PREFIX, DESTDIR, AWNPREFIX, CAIRODOCKPREFIX"

# install
install:

	-install -d $(DESTDIR)/etc/gnomenu $(DESTDIR)$(PREFIX)/bin/ $(DESTDIR)$(LIBDIR) \
	$(DESTDIR)$(PREFIX)/share $(DESTDIR)$(LIBDIR)/bonobo/servers $(DESTDIR)$(CAIRODOCKPREFIX)/share/cairo-dock/plug-ins/Dbus/third-party/GnoMenu $(DESTDIR)$(PREFIX)/share/kde4/apps/plasma
	@echo $(PREFIX) > $(DESTDIR)/etc/gnomenu/prefix
	python -u setup.py
	
	#-install src/bin/GnoMenu.py $(DESTDIR)$(PREFIX)/bin/
	-cp -r src/lib/gnomenu $(DESTDIR)$(LIBDIR)
	-cp -r src/share/gnomenu $(DESTDIR)$(PREFIX)/share
	-cp -r src/share/avant-window-navigator $(DESTDIR)$(AWNPREFIX)/share
	-install src/share/dockmanager/scripts/GnoMenu.py $(DESTDIR)$(DOCKYPREFIX)/share/dockmanager/scripts/
	-cp -r src/share/dockmanager/scripts/GnoMenu $(DESTDIR)$(DOCKYPREFIX)/share/dockmanager/scripts/
	#-cp -r src/share/xfce4 $(DESTDIR)$(PREFIX)/share
	-cp -r src/share/locale $(DESTDIR)$(PREFIX)/share
	#-cp -r src/share/plasma/plasmoids $(DESTDIR)$(PREFIX)/share/kde4/apps/plasma
	-install src/share/cairo-dock/third-party/GnoMenu/* $(DESTDIR)$(CAIRODOCKPREFIX)/share/cairo-dock/plug-ins/Dbus/third-party/GnoMenu/
	#-cp -r src/share/cairo-dock ~/.config/
	-install src/bin/GnoMenu.py $(DESTDIR)$(PREFIX)/bin/
	-install src/lib/bonobo/GNOME_GnoMenu.server $(DESTDIR)$(LIBDIR)/bonobo/servers
	-plasmapkg -i src/share/plasma/plasmoids/GnoMenu.zip -p $(DESTDIR)$(PREFIX)/share/kde4/apps/plasma/plasmoids
	@echo "Makefile: GnoMenu installed."


# uninstall
uninstall:

	rm -rf $(LIBDIR)/gnomenu
	rm -rf $(PREFIX)/share/gnomenu
	rm -rf $(PREFIX)/share/avant-window-navigator/applets/GnoMenu.desktop
	rm -rf $(PREFIX)/share/avant-window-navigator/applets/GnoMenu
	#rm -rf $(PREFIX)/share/xfce4/panel-plugins/GnoMenu.desktop
	rm -rf $(PREFIX)/bin/GnoMenu.py
	rm -rf $(PREFIX)/share/kde4/apps/plasma/plasmoids/GnoMenu
	rm -rf $(LIBDIR)/bonobo/servers/GNOME_GnoMenu.server
	rm -rf /etc/gnomenu/prefix
	rm -rf ~/.gnomenu
	rm -rf ~/.config/cairo-dock/third-party/GnoMenu
	rm -rf $(PREFIX)/share/dockmanager/scripts/GnoMenu
	rm -rf $(PREFIX)/share/dockmanager/scripts/GnoMenu.py
	plasmapkg -r GnoMenu


