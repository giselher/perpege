from engine.Object import MovableObject
from reader import Reader
import pygame
import random

READER = Reader('content/story/dialogs/')

class SAS:
    pass

class Actor(MovableObject, SAS):

    def __init__(self, portrait, animations, position, col_rect, actor_data=None):
        MovableObject.__init__(self, animations['down'][3], position, col_rect)
        
        self.portrait = portrait
        
        if actor_data is not None:
            self.name = actor_data['name']
            self.dialogs = {}
            for dialog in actor_data['dialogs']:
                _dialog = dialog.strip()
                _dlg = READER.readFile(_dialog)
                self.dialogs[_dialog] = _dlg
        
        self.id = actor_data
        
        self.diff_x = self.crect.x - self.rect.x
        self.diff_y = self.crect.y - self.rect.y    

        self.animations = animations
        self.directions = { 'up' : [0, -1],
                            'down' : [0, 1],
                            'left' : [-1, 0],
                            'right' : [1, 0],
                            'none' : [0, 0]}
       #temporarly
        self.step = 5 
        self.a_step = 0
        self.i_step = 0
        self.prev_dir = 'none' 
        
    def clamp(self, rect):
        self.rect.clamp_ip(rect)
        self.crect.topleft = (self.rect.x+self.diff_x, self.rect.y+self.diff_y)
        
    def action(self, target):
        pass
        
    def facing(self, target):
        if target.crect.center[0] < self.crect.center[0]:
            if target.crect.center[1] < self.crect.center[1]:
                if (self.crect.center[0] - target.crect.center[0]) < \
                        (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['left'][3]
            else:
                if (self.crect.center[0] - target.crect.center[0]) < \
                        (target.crect.center[1] - self.crect.center[1]):
                    self.image = self.animations['down'][3]
                else:
                    self.image = self.animations['left'][3]
        else:
            if target.crect.center[1] < self.crect.center[1]:
                if (target.crect.center[0] - self.crect.center[0]) < \
                        (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['right'][3]
            else:
                if (target.crect.center[0] - self.crect.center[0]) < \
                        (target.crect.center[1] - self.crect.center[1]):
                    self.image = self.animations['down'][3]
                else:
                    self.image = self.animations['right'][3]
        
    def move(self, coord):
        crect = self.crect.move(coord)
        return {'new_crect' : crect, 'old_crect' : self.crect}
        
    def animate(self, direction):
        """
        up, down, left, right, ...
        """
        if direction == self.prev_dir:
            if self.a_step == 1:
                self.i_step += 1
                self.a_step = 0
            else:
                self.a_step += 1
        else:
            self.a_step = 0
            self.i_step = 0
            self.prev_dir = direction
        try:
            self.image = self.animations[direction][self.i_step]
        except IndexError:
            self.i_step = 0
            
    def loop(self, world):
        _choice = self.prev_dir
        direction = self.directions[_choice]
        direction = [direction[0]*self.step, direction[1]*self.step]
        self.crect = world.check_collision(self, self.move(direction))
    
        self.rect.topleft = (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

        
class Player(Actor):
    
    def __init__(self, portrait, animations, position, col_rect):
        Actor.__init__(self, portrait, animations, position, col_rect)
        
        self.name = "Yves"
        
        self.events = []
        self.quest_events = {}

    def setCenter(self, coord):
        self.rect.center = coord
        self.crect.topleft = (self.rect.x+self.diff_x, self.rect.y+self.diff_y)

    def loop(self):
        self.rect.topleft = (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

