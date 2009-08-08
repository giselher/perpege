from engine.Object import MovableObject
import pygame

import random

class SAS:
    pass

class Actor(MovableObject, SAS):

    def __init__(self, animations, position, col_rect, sas=None, ta=None):
        MovableObject.__init__(self, animations['down'][3], position, col_rect)
        
        self.diff_x = self.crect.x - self.rect.x
        self.diff_y = self.crect.y - self.rect.y    

        self.animations = animations
        self.directions = { 'up' : [0, -1],
                            'down' : [0, 1],
                            'left' : [-1, 0],
                            'right' : [1, 0],
                            'none' : [0, 0]}
        self.step = 5 
        self.a_step = 0
        self.i_step = 0
        self.prev_dir = 'none' 
        
    def facing(self, target):
        if target.crect.center[0] < self.crect.center[0]:
            if target.crect.center[1] < self.crect.center[1]:
                if (self.crect.center[0] - target.crect.center[0]) < (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['left'][3]
            else:
                if (self.crect.center[0] - target.crect.center[0]) < (target.crect.center[1] - self.crect.center[1]):
                    self.image = self.animations['down'][3]
                else:
                    self.image = self.animations['left'][3]
        else:
            if target.crect.center[1] < self.crect.center[1]:
                if (target.crect.center[0] - self.crect.center[0]) < (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['right'][3]
            else:
                if (target.crect.center[0] - self.crect.center[0]) < (target.crect.center[1] - self.crect.center[1]):
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
        #self.animate(_choice) 
        direction = self.directions[_choice]
        direction = [direction[0]*self.step, direction[1]*self.step]
        self.crect = world.check_collision(self, self.move(direction))
    
        self.rect.topleft = (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

        
class Player(Actor):
    
    def __init__(self, animations, position, col_rect, sas=None):
        Actor.__init__(self, animations, position, col_rect)

    def setCenter(self, coord):
        self.rect.center = coord
        self.crect.topleft = (self.rect.x+self.diff_x, self.rect.y+self.diff_y)

    def loop(self):
        self.rect.topleft = (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

