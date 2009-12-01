"""
@author Alexander Preisinger


 
"""
import pygame

class I2d2axis(object):
    
    def __init__(self, key_map):
        self.up = key_map["up"]
        self.down = key_map["down"]
        self.right = key_map["right"]
        self.left = key_map["left"]
        
    def loop(self, step):
        """
        """
        keystate = pygame.key.get_pressed()
        x = keystate[self.right] - keystate[self.left]
        y = keystate[self.down] - keystate[self.up]
        if x: return [x*step, 0]
        else: return [0, y*step]
    
    def __call__(self, step):
        return self.loop(step)
        
class I2d4axis(object):
    
    def __init__(self, key_map):
        self.up = key_map["up"]
        self.down = key_map["down"]
        self.right = key_map["right"]
        self.left = key_map["left"]
        
    def loop(self, step):
        keystate = pygame.key.get_pressed()
        x = keystate[self.right] - keystate[self.left]
        y = keystate[self.down] - keystate[self.up]
        if x and y:
            step = int(float(step) * 0.7071)
        return [x*step, y*step]       

    def __call__(self, step):
        return self.loop(step)