"""
@author Alexander Preisinger


 
"""
import Object

import pygame as pg

class I2d2axis(object):
        
    def loop(self, step):
        """
        """
        keystate = pg.key.get_pressed()
        x = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        y = keystate[pg.K_DOWN] - keystate[pg.K_UP]
        if x: return[x*step, 0]
        else: return[0, y*step]
    
    def __call__(self, step):
        self.loop(step)
        
class I2d4axis(object):
        
    def loop(self, step):
        keystate = pg.key.get_pressed()
        x = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        y = keystate[pg.K_DOWN] - keystate[pg.K_UP]
        if x and y:
            step = int(float(step) * 0.70710)
        return [x*step, y*step]        

    def __call__(self, step):
        self.loop(step)