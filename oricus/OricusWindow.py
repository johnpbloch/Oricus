# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import locale
import subprocess
from locale import gettext as _
locale.textdomain('oricus')

from gi.repository import Gtk, GObject # pylint: disable=E0611
import logging
logger = logging.getLogger('oricus')

from oricus_lib import Window
from oricus_lib import Apache
from oricus.AboutOricusDialog import AboutOricusDialog
from oricus.PreferencesOricusDialog import PreferencesOricusDialog

# See oricus_lib.Window.py for more details about how this class works
class OricusWindow(Window):
    __gtype_name__ = "OricusWindow"
    done_setting_up = False
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(OricusWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutOricusDialog
        self.PreferencesDialog = PreferencesOricusDialog

        # Code for other initialization actions should be added here.
        if not Apache.is_installed():
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                Gtk.ButtonsType.YES_NO, _("Apache is not installed. Would you like to intall it?"))
            response = dialog.run()
            if response == Gtk.ResponseType.NO:
                sys.exit()
            worked = subprocess.call(['/usr/bin/gksu', '/usr/bin/apt-get install apache2'])
            if worked > 0:
                sys.exit()
            dialog.destroy()
        
        self.status = OricusWindowStatusBar(self.builder.get_object('statusbar1'))
        
        self.builder.get_object('statusToggleSwitch').set_active(Apache.is_running())
        self.status.set(Apache.get_status(), StatusTypes.STARTUP)
        self.status.clear(StatusTypes.STARTUP, 5000)
        self.done_setting_up = True
    
    def on_statusToggleSwitch_notify(self, widget, user_data=None):
        if not user_data.name == 'active':
            return
        if not self.done_setting_up:
            return
        if widget.get_active() and not Apache.is_running():
            self.status.set(_("Starting Apache..."), StatusTypes.TOGGLE);
            Apache.start()
            self.status.clear(StatusTypes.TOGGLE)
        else:
            self.status.set(_("Stopping Apache..."), StatusTypes.TOGGLE);
            Apache.stop()
            self.status.clear(StatusTypes.TOGGLE)

class OricusWindowStatusBar():
    statusbar = None
    
    def __init__(self, statusbar):
        self.statusbar = statusbar
        
    def set(self, message, context=None):
        if context is None:
            context = StatusTypes.DEFAULT
        self.statusbar.push(context, message)

    def clear(self, context=None, Delay=None):
        if context is None:
            context = StatusTypes.DEFAULT
        if Delay is None:
            self.statusbar.pop(context)
            return False
        try:
            GObject.timeout_add(Delay, self.clear, context)
        except:
            pass
        
class StatusTypes():
    (DEFAULT,
     STARTUP,
     TOGGLE) = range(1, 4)
