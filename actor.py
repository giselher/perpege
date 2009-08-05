from engine.Object import MovableObject
import pygame

import random

class SAS:
    pass

class Actor(MovableObject, SAS):

    def __init__(self, animations, position, col_rect, sas_id=None):
        MovableObject.__init__(self, pygame.Surface((0, 0)), position, col_rect)
        self.id = sas_id
        
        self.animations = animations
        self.choices = ['left', 'right', 'up', 'down']
        self.directions = { 'up' : [0, -1],
                            'down' : [0, 1],
                            'left' : [-1, 0],
                            'right' : [1, 0]}
        self.step = 6
        self.w_step = 0    
        self.i_step = 0
        self.a_step = 0
        self.prev_dir = 'right'
        
    def collision_prediction(self):
        pass
        
    def animate(self, dir):
        if dir == self.prev_dir:
            if self.w_step > 2:
                self.w_step = 0
                self.i_step += 1
            else:
                self.w_step += 1
        else:
            self.w_step = 0
            self.i_step = 0
        try:
            self.image = self.animations[dir][self.i_step]
        except IndexError:
            self.i_step = 0
            
    def loop(self):
        _choice = self.prev_dir
        self.animate(_choice)
        direction = self.directions[_choice]
        direction = [direction[0]*self.step, direction[1]*self.step]
        self.rect.move_ip(direction)
        self.crect.move_ip(direction)
        
class Player(Actor):
    
    def __init__(self):
        Actor.__init__(self)
