#!/usr/bin/env python
import os, sys
import pygame
from pygame.locals import *
import engine, settings
from engine.Misc import loadImage
from map import World
from gui.menu import MainMenu

from gui.debug import blit_fps

class StateHandler(object):
    
    def __init__(self, state):
        self.state = state
        self.previous = None
        
    def change(self, state):
        self.previous = self.state
        self.state = state

    def set_state_game(self):
        self.previous = self.state
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
    menu = MainMenu(State, 'menu.jpg')
    
    menu.store_action('new_game', State.set_state_game)
    menu.store_action('quit', quit)

    input = engine.I2d4axis()

    while True:
        screen.fill((0, 0, 0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT: quit()
            elif event.type == KEYDOWN:
                if event.key == K_q: quit()
                else:
                    pygame.event.post(event)
            else:
                pygame.event.post(event)
            
        _state = State.state
        if _state == 'game':
            world.key_loop()
            world.loop()
            world.move(input.loop(-15))
            world.draw()
        elif _state == 'menu':
            menu.key_loop()
            menu.draw(screen)

        blit_fps(clock, screen, (10, 10))
        _display_flip()
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt, message:
        print "KeyboardInterrupt", message
