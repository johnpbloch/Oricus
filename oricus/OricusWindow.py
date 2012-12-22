# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import locale
import subprocess
from locale import gettext as _
locale.textdomain('oricus')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('oricus')

from oricus_lib import Window
from oricus.AboutOricusDialog import AboutOricusDialog
from oricus.PreferencesOricusDialog import PreferencesOricusDialog

# See oricus_lib.Window.py for more details about how this class works
class OricusWindow(Window):
    __gtype_name__ = "OricusWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(OricusWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutOricusDialog
        self.PreferencesDialog = PreferencesOricusDialog

        # Code for other initialization actions should be added here.
        try:
            output = subprocess.check_output(['/usr/sbin/service', 'apache2', 'status']);
            isError = False
        except subprocess.CalledProcessError, e:
            output = e.output
            isError = True
        self.builder.get_object('statusToggleSwitch').set_active(not isError)
        if isError:
            self.builder.get_object('statusbar1').push(1, output.strip())

