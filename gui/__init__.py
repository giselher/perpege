"""
Perpeg gui elements.
"""
import sys
sys.path.append('../')
from engine.Misc import loadImage
from dialog import Dialog
import pygame
from pygame.locals import *


class Interface(object):
    
    def __init__(self, world, display):
        self.world = world
        self.display = display
        self.dialog = Dialog(self, display)
        self.state = ''
        
    def showDialog(self, owner, player, handler):
        self.dialog.initDialog(owner, player, handler)        
        self.state = 'dialog'
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_a:
                    if not self.dialog.next(): self.world.itf = False
        
    def draw(self):
        if self.state == 'dialog':
            self.dialog.draw()