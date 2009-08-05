#!/usr/bin/env python
import os, sys
import pygame
from pygame.locals import *
import engine, settings
from engine.Misc import loadImage
from reader import Reader
from map import MapMaker, World
from gui.menu import MainMenu

class StateHandler(object):
    
    def __init__(self, state):
        self.state = state
        
    def change(self, state):
        self.state = state
        
    def set_state_game(self):
        self.state = 'game'
        
    def __str__(self):
        return self.state
    
    def _repr__(self):
        return self.state

def init():
    pygame.init()
    settings.init()
    screen = pygame.display.set_mode(settings.gettuple("display", "resolution"))
    if settings.getbool("display", "fullscreen"): pygame.display.toggle_fullscreen()
    pygame.display.set_caption("Perpege Re-Write")
    pygame.display.set_icon(loadImage("icon.png"))
    return screen

def quit():
    settings.quit()
    pygame.quit()
    sys.exit(0)

def main():
    screen = init()
    _display_flip = pygame.display.flip
    screen.blit(loadImage('Load.png'), (0, 0))
    _display_flip()
    clock = pygame.time.Clock()
    
    State = StateHandler('menu')
    
    world = World(screen, State) 
    menu = MainMenu(screen)


    MapReader = Reader('./content/maps/')
    map_data = MapReader.readFile('01_test.map')
    map_maker = MapMaker(world)
    map_maker.makeMap(map_data)

    input = engine.I2d4axis()

    menu.store_action('new_game', State.set_state_game)
    while True:
        screen.fill((0, 0, 0))
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == QUIT: quit()
            elif event.type == KEYDOWN:
                if event.key == K_q: quit()
##                elif event.key == K_F3:
##                    sys.path.append('../tools/')
##                    import collrectsetter as crs
##                    crs.main()
##                    init()
                elif event.key == K_r:
                    Map_Maker.makeMap(map_data)
                else:
                    pygame.event.post(event)
            else:
                pygame.event.post(event)
            
        _state = str(State)
        if _state == 'game':
            world.key_loop()
            world.move(input.loop(-20))
            world.draw()
        elif _state == 'menu':
            menu.key_loop()
            menu.draw()

        _display_flip()
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt, message:
        print "KeyboardInterrupt", message



