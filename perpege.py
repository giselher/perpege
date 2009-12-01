#!/usr/bin/env python
import os
import sys
import pygame
import settings
from pygame.locals import *
from engine.Misc import loadImage
from world import World
from gui.debug import blit_fps, blit_grid

def init():
    pygame.init()
    settings.init()
    screen = pygame.display.set_mode(settings.get_tuple("display", "resolution"))
    if settings.get_bool("display", "fullscreen"): pygame.display.toggle_fullscreen()
    pygame.display.set_caption("Perpege Pre-Alpha")
    pygame.display.set_icon(loadImage("icon.png"))
    return screen

def quit():
    settings.quit()
    pygame.quit()
    print "Ended succesfully."
    sys.exit()
    
def main():
    screen = init() 
    _display_flip = pygame.display.flip
    screen.blit(loadImage('Load.png'), (0, 0))
    _display_flip()
    clock = pygame.time.Clock()

    world = World(screen, settings) 
    
    SCREENSHOT = settings.get_key('screenshot') 
    TF = settings.get_key('toggle_fullscreen')

    world.interface.menu.store_action('quit', quit)
    _post = pygame.event.post
    while True:
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == QUIT: 
                quit()
            elif event.type == KEYDOWN:
                if event.key == SCREENSHOT: 
                    pygame.image.save(screen.copy(), 'screenshot.jpg')
                elif event.key == TF:
                    pygame.display.toggle_fullscreen()
                else:
                    _post(event)
            else:
                _post(event)
                
        screen.fill((0, 0, 0))
        
        world.loop()   
            
        if not '--no-fps' in sys.argv: 
            blit_fps(clock, screen, (10, 10))
        if '--grid' in sys.argv:
            blit_grid(screen, 2)
        
        
        _display_flip()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "KeyboardInterrupt"