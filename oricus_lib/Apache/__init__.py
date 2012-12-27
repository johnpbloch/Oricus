import subprocess
import re
import os
from oricus_lib.Sudo import sudo

__apache_conf_dir__ = '/etc/apache2'

def get_conf_dir(plus=None):
    confdir = __apache_conf_dir__
    if not plus is None:
        confdir = os.path.join(confdir, plus)
    return confdir

def is_installed():
    find_apache = subprocess.call('/usr/bin/which apache2ctl > /dev/null', shell=True)
    return True if find_apache == 0 else False

def get_status():
    try:
        return subprocess.check_output(['/usr/sbin/service', 'apache2', 'status']).strip()
    except subprocess.CalledProcessError, e:
        return e.output.strip()

def is_running():
    output = get_status()
    return True if re.search('Apache2 is running \(pid \d+\)', output) else False

def start():
    sudo(['/usr/sbin/service', 'apache2', 'start'], Desc="Start Apache")

def stop():
    sudo(['/usr/sbin/service', 'apache2', 'stop'], Desc="Stop Apache")

def restart():
    sudo(['/usr/sbin/service', 'apache2', 'restart'], Desc="Restart Apache")