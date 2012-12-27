import os
from oricus_lib import Apache
from oricus_lib.Apache.Vhosts.Vhost import Vhost

def import_all():
    sites_available = Apache.get_conf_dir('sites-available')
    all_sites = [ f for f in os.listdir(sites_available) if os.path.isfile(os.path.join(sites_available, f)) ]
    for site in all_sites:
        Vhost(site).import_config()
