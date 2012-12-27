import subprocess

def sudo(Command, Desc=None):
    cmd = ['/usr/bin/gksu', '--sudo-mode']
    if not Desc is None:
        cmd += ['--description', Desc]
    return _do_su_cmd(Command, cmd)

def su(Command, Desc=None):
    cmd = ['/usr/bin/gksu', '--su-mode']
    if not Desc is None:
        cmd += ['--description', Desc]
    return _do_su_cmd(Command, cmd)

def _do_su_cmd(Command, Setup):
    if type(Command) is list:
        cmd = Setup + Command
    elif type(Command) is str:
        Setup.append(Command)
        cmd = Setup
    else:
        raise Exception, "Bad command format!"
    return subprocess.call(cmd)
    
    