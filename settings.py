import os
import sys
from engine import setImagePath
from ConfigParser import ConfigParser
from pygame.locals import *

class Settings(object):

    def __init__(self):
        self.__parser = ConfigParser()

        if os.name == 'posix':
            self.path = os.path.join(os.environ['HOME'], '.perpege')
        else:
            self.path = os.path.join(os.path.abspath('.'), 'settings.ini')

        if not os.path.exists(self.path):
            self.__write()

        self.__parser.read(self.path)

        setImagePath('./content/')

    def __write(self):
        cfg_file = open(self.path, 'w')
        default_file = open('./content/default.conf', 'r')
        cfg_file.write(default_file.read())
        default_file.close()
        cfg_file.close()

    def get_key_map(self):
        key_map = {}
        for key, value in self.__parser.items('controls'):
            key_map[key] = eval(value)
        return key_map

    def get_key(self, key):
        return eval(self.__parser.get('controls', key))

    def get_tuple(self, section, key):
        raw_value = self.__parser.get(section, key)
        return eval('tuple(%s)' % raw_value)

    def get_bool(self, section, key):
        return self.__parser.getboolean(section, key)

    def quit(self):
        cfg_file = open(self.path, 'w')
        self.__parser.write(cfg_file)
        cfg_file.close()