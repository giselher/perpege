"""
@author Alexander Preisinger


 
"""
import pygame

class I2d2axis(object):
        
    def loop(self, step):
        """
        """
        keystate = pygame.key.get_pressed()
        x = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        y = keystate[pygame.K_DOWN] - keystate[pygame.K_UP]
        if x: return[x*step, 0]
        else: return[0, y*step]
    
    def __call__(self, step):
        return self.loop(step)
        
class I2d4axis(object):
        
    def loop(self, step):
        keystate = pygame.key.get_pressed()
        x = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        y = keystate[pygame.K_DOWN] - keystate[pygame.K_UP]
        if x and y:
            step = int(float(step) * 0.70710)
        return [x*step, y*step]        

    def __call__(self, step):
        return self.loop(step)