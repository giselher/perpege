import os, sys
from engine import setImagePath
from ConfigParser import ConfigParser 

VERSION = '0.0.1'

def __getPath():
    os_name = sys.platform
    if os_name == 'linux2':
        cfg_path = os.path.join(os.environ['HOME'], '.perpege')
    else:
        cfg_path = os.path.join(os.path.abspath('.'), 'settings.ini')
    return cfg_path

__cp = ConfigParser()
__cp_path = __getPath()

def __cfg_write():
    __cp.add_section('display')
    __cp.set('display', 'fullscreen', False)
    __cp.set('display', 'resolution', (1024, 768))
    __cp.add_section('game')
    __cp.set('game', 'version', VERSION)
    cfg_file = open(__cp_path, 'w')
    __cp.write(cfg_file)
    cfg_file.close()

def init():
    global __cp, __cp_path
    if not os.path.exists(__cp_path):
        __cfg_write()
    else:
        __cp.read(__cp_path)
        if not __cp.has_option('game', 'version'):
            __cp.set('display', 'resolution', (1024, 768))
            __cp.add_section('game')
            __cp.set('game', 'version', VERSION)
    setImagePath('./content/')

def gettuple(section, key):
    global __cp
    value = __cp.get(section, key)
    value_list = value.replace('(', '').replace(')', '').split(',')
    return (int(value_list[0]), int(value_list[1]))

def getbool(section, key):
    global __cp
    return __cp.getboolean(section, key)

def quit():
    global __cp, __cp_path
    cfg_file = open(__cp_path, 'w')
    __cp.write(cfg_file)
    cfg_file.close()