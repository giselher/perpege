#!/usr/bin/env python
import os, sys
import pygame
from pygame.locals import *
import settings
from engine.Misc import loadImage
from world import World
from gui.menu import MainMenu
from gui.debug import blit_fps
from gui.dialog import Dialog

class StateHandler(object):
    
    def __init__(self, state):
        self.state = state
        self.previous = None
        
    def change(self, state):
        self.previous = self.state
        self.state = state
        
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
    
    def new_game():
        State.change('game')
        
    world = World(screen, State) 
    menu = MainMenu(State, 'menu.jpg')
    
    menu.store_action('new_game', new_game)
    menu.store_action('quit', quit)
    _post = pygame.event.post
    while True:
        screen.fill((0, 0, 0))
        clock.tick(35)
        for event in pygame.event.get():
            if event.type == QUIT: quit()
            elif event.type == KEYDOWN:
                if event.key == K_q: quit()
                elif event.key == K_F11: pygame.display.toggle_fullscreen()
                else:
                    _post(event)
            else:
                _post(event)
            
        _state = State.state
        if _state == 'game':
            world.loop()         
        elif _state == 'menu':
            menu.draw(screen)

        blit_fps(clock, screen, (10, 10))
        _display_flip()
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
