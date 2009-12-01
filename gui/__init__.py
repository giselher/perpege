"""
Perpeg gui elements.
"""
import sys
sys.path.append('../')
import pygame
from engine.Misc import loadImage
from dialog import Dialog
from menu import MainMenu
from combat import Combat
from pygame.locals import *

class EmptyEvent():
    
    def __init__(self):
        self.type = None
        self.key = None

class Interface(object):
    
    def __init__(self, world, display):
        self.world = world
        self.display = display
        self.menu = MainMenu(self)
        self.combat = Combat(self, display)
        self.dialog = Dialog(self, display)
        self.state = ''
        
    def showDialog(self, owner, player, handler):
        self.dialog.initDialog(owner, player, handler)        
        self.state = 'dialog'
        self.world.state = 'itf'
        
    def showMenu(self, state='game'):
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