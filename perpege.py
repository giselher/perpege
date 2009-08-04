#!/usr/bin/env python
import os, sys
import pygame as pg
from pygame.locals import *
import engine, settings
from engine.Misc import loadImage
from reader import Reader
from map import MapMaker, World

def init():
    pg.init()
    settings.init()
    screen = pg.display.set_mode(settings.geteval("display", "resolution"))
    if settings.getbool("display", "fullscreen"): pg.display.toggle_fullscreen()
    pg.display.set_caption("Perpege Re-Write")
    pg.display.set_icon(loadImage("icon.png"))
    return screen

def quit():
    settings.quit()
    pg.quit()
    sys.exit(0)

def main():
    screen = init()
    _display_flip = pg.display.flip
    screen.blit(loadImage("Load.png"), (0, 0))
    _display_flip()
    clock = pg.time.Clock()
    _MapReader = Reader("./content/maps/")
    map_data = _MapReader.readFile("01_test.map")
    world = World(screen) 
    Map_Maker = MapMaker(world)
    Map_Maker.makeMap(map_data)
    input = engine.I2d4axis()
    while True:
        screen.fill((0, 0, 0))
        clock.tick(50)
        for event in pg.event.get():
            if event.type == QUIT: quit()
            elif event.type == KEYDOWN:
                if event.key == K_q: quit()
                elif event.key == K_F3:
                    import engine.colrectsetter as crs
                    crs.main()
                    init()
                elif event.key == K_r:
                    Map_Maker.makeMap(map_data)
            
        world.move(input.loop(-20))
        world.draw()
        _display_flip()
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt, message:
        print "KeyboardInterrupt", message


