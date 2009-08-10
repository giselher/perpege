"""
Perpeg gui elements.
"""
import sys
sys.path.append('../')
from engine.Misc import loadImage
from dialog import Dialog
from menu import MainMenu
import pygame
from pygame.locals import *


class Interface(object):
    
    def __init__(self, world, display):
        self.world = world
        self.display = display
        self.menu = MainMenu(self)
        self.dialog = Dialog(self, display)
        self.state = ''
        
    def showDialog(self, owner, player, handler):
        self.dialog.initDialog(owner, player, handler)        
        self.state = 'dialog'
        self.world.itf = True
        
    def showMenu(self, state='game'):
        self.menu.set_state(state)
        self.state = 'menu'
        self.world.itf = True
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return event.key
        
    def draw(self):
        if self.state == 'menu':
            self.menu.key_loop(self.key_loop())
            self.menu.draw(self.display)
        elif self.state == 'dialog':
            self.dialog.key_loop(self.key_loop())
            self.dialog.draw()