"""
Perpeg gui elements.
"""
import sys
sys.path.append('../')
import pygame
from engine.Misc import loadImage
from dialog import Dialog
from menu import MainMenu
from pygame.locals import *

class EmptyEvent():

    def __init__(self):
        self.type = None
        self.key = None

class Interface(object):

    def __init__(self, world):
        self.world = world
        self.load_image = self.world.load_image
        self.display = world.display
        self.menu = MainMenu(self)
        self.dialog = Dialog(self, self.display)
        self.state = ''

    def show_dialog(self, owner, player, handler):
        self.dialog.init_dialog(owner, player, handler)
        self.state = 'dialog'
        self.world.state = 'itf'

    def show_menu(self, state='game'):
        self.menu.set_state(state)
        self.state = 'menu'
        self.world.state = 'itf'

    def return_event(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return event
        else:
            return EmptyEvent()

    def draw(self):
        if self.state == 'menu':
            self.menu.key_loop(self.return_event())
            self.menu.draw(self.display)
        elif self.state == 'dialog':
            self.dialog.key_loop(self.return_event())
            self.dialog.draw()
        else:
            self.world.state = 'game'