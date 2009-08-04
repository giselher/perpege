import os, sys
from engine import setImagePath
from ConfigParser import ConfigParser 


def __getPath():
    os_name = sys.platform
    if os_name == "linux2":
        cfg_path = os.path.join(os.environ["HOME"], ".perpege")
    else:
        cfg_path = os.path.join(os.path.abspath("."), "settings.ini")
    return cfg_path

__cp = ConfigParser()
__cp_path = __getPath()

def init():
    global __cp, __cp_path
    if not os.path.exists(__cp_path):
        cfg_file = open(__cp_path, "w")
        __cp.add_section("display")
        __cp.set("display", "fullscreen", False)
        __cp.set("display", "resolution", (800, 600))
        __cp.write(cfg_file)
        cfg_file.close()
    else:
        __cp.read(__cp_path)
        
    #only for current working
    setImagePath("./content/")


def geteval(section, key):
    """
    DEPTRECATED!!!
    Don't call this! Could be dangerous and security risk
    Should make gettuple or getlist functions to replace this function!
    """
    global __cp
    return eval(__cp.get(section, key))

def getbool(section, key):
    global __cp
    return __cp.getboolean(section, key)

def quit():
    global __cp, __cp_path
    cfg_file = open(__cp_path, "w")
    __cp.write(cfg_file)
    cfg_file.close()
        

