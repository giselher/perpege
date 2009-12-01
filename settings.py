import os
import sys
from engine import setImagePath
from ConfigParser import ConfigParser 
from pygame.locals import *

VERSION = '0.0.2'

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
    global __cp_path
    cfg_file = open(__cp_path, 'w')
    default_file = open('./content/default.conf', 'r')
    cfg_file.write(default_file.read())
    default_file.close()
    cfg_file.close()

def init():    
    global __cp, __cp_path
    if not os.path.exists(__cp_path):
        __cfg_write()
        __cp.read(__cp_path)
    else:
        __cp.read(__cp_path)
        if not __cp.has_option('game', 'version'):
            __cp.set('display', 'resolution', (1024, 768))
            __cp.add_section('game')
            __cp.set('game', 'version', VERSION)
    setImagePath('./content/')
    
def get_key_map():
    global __cp
    key_map = {}
    for key, value in __cp.items('controls'):
        key_map[key] = eval(value)
    return key_map
    
def get_key(key):
    global __cp
    return eval(__cp.get('controls', key))

def get_tuple(section, key):
    global __cp
    raw_value = __cp.get(section, key)
    return eval('tuple(%s)' % raw_value)

def get_bool(section, key):
    global __cp
    return __cp.getboolean(section, key)

def quit():
    global __cp, __cp_path
    cfg_file = open(__cp_path, 'w')
    __cp.write(cfg_file)
    cfg_file.close()