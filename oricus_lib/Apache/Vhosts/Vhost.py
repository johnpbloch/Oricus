from oricus_lib import Apache
import os
import re

class Vhost(object):
    __config_values = {}
    __current_block = None
    __in_vhost_block = False
    __finished_with_vhost = False
    
    def __init__(self, filename):
        self.filename = filename

    def import_config(self):
        with open(os.path.join(Apache.get_conf_dir('sites-available'), self.filename), 'r') as f:
            for line in f:
                if not self.__finished_with_vhost:
                    self.parse_line(line)

    def parse_line(self, line):
        line = line.strip()
        if (not self.__in_vhost_block) and re.search('<virtualhost ([^>]+)>', line, re.IGNORECASE):
            self.__in_vhost_block = True
        if not self.__in_vhost_block:
            return
        if re.search('</virtualhost>', line, re.IGNORECASE):
            self.__finished_with_vhost = True
            return
        # Parse input