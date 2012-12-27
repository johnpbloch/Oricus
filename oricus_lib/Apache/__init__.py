import subprocess
import re

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
    subprocess.call(['/usr/bin/gksu', '/usr/sbin/service', 'apache2', 'start'])

def stop():
    subprocess.call(['/usr/bin/gksu', '/usr/sbin/service', 'apache2', 'stop'])

def restart():
    subprocess.call(['/usr/bin/gksu', '/usr/sbin/service', 'apache2', 'restart'])