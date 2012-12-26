# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import locale
import subprocess
from locale import gettext as _
locale.textdomain('oricus')

from gi.repository import Gtk, GObject # pylint: disable=E0611
import logging
logger = logging.getLogger('oricus')

from oricus_lib import Window
from oricus.AboutOricusDialog import AboutOricusDialog
from oricus.PreferencesOricusDialog import PreferencesOricusDialog

# See oricus_lib.Window.py for more details about how this class works
class OricusWindow(Window):
    __gtype_name__ = "OricusWindow"
    STATUS_TYPE_STARTUP = 24
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(OricusWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutOricusDialog
        self.PreferencesDialog = PreferencesOricusDialog

        # Code for other initialization actions should be added here.
        find_apache = subprocess.call('/usr/bin/which apache2ctl > /dev/null', shell=True)
        if find_apache > 0:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                Gtk.ButtonsType.YES_NO, "Apache is not installed. Would you like to intall it?")
            response = dialog.run()
            if response == Gtk.ResponseType.NO:
                import sys
                sys.exit()
            worked = subprocess.call(['/usr/bin/gksu', '/usr/bin/apt-get install apache2'])
            if worked > 0:
                import sys
                sys.exit()
            dialog.destroy()
        try:
            output = subprocess.check_output(['/usr/sbin/service', 'apache2', 'status']);
            isError = False
        except subprocess.CalledProcessError, e:
            output = e.output
            isError = True
        self.builder.get_object('statusToggleSwitch').set_active(not isError)
        self.builder.get_object('statusbar1').push(self.STATUS_TYPE_STARTUP, output.strip())
        GObject.timeout_add(5000, self.clear_status, self.STATUS_TYPE_STARTUP)

    def clear_status(self, context_id):
        self.builder.get_object('statusbar1').pop(context_id)
        return False

