#!/usr/bin/python
import os
import sys
import pygame
from settings import Settings
from pygame.locals import *
from engine.Misc import loadImage
from world import World
from gui.debug import blit_fps, blit_grid

try:
    import psyco
    psyco.log()
    psyco.profile()
except ImportError:
    print("Please install psyco for a better performance.")

def init():
    global settings
    pygame.init()
    settings = Settings()

    screen = \
        pygame.display.set_mode(settings.get_tuple("display", "resolution"))

    if settings.get_bool("display", "fullscreen"):
        pygame.display.toggle_fullscreen()

    pygame.display.set_caption("Perpege Alpha")
    pygame.display.set_icon(loadImage("icon.png"))
    return screen

def quit():
    settings.quit()
    pygame.quit()
    #print("Ended succesfully.")
    sys.exit(0)

def main():
    screen = init()

    # This is faster because of a direct reference to the functions
    _display_flip = pygame.display.flip
    _event_get = pygame.event.get
    _post = pygame.event.post
    _fill = screen.fill

    screen.blit(loadImage('Load.png'), (0, 0))
    _display_flip()
    clock = pygame.time.Clock()

    world = World(screen, settings)
    _loop = world.loop

    SCREENSHOT = settings.get_key('screenshot')
    TF = settings.get_key('toggle_fullscreen')

    world.interface.menu.store_action('quit', quit)

    while True:
        clock.tick(100)

        for event in _event_get():
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

        _fill((0, 0, 0))

        _loop()

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
