from actor import Actor
from reader import Reader
from engine.Decorator import Cache, Log
from engine.Object import ImmobileObject, MovableObject, AnimatedObject
from engine.Misc import loadImage, getImagePath
import pygame
from pygame.locals import *
import gzip, os.path, pickle
import threading
         

class World(pygame.sprite.Sprite):
    
    def __init__(self, display_surface, state_handler):
        pygame.sprite.Sprite.__init__(self)
        self.state = state_handler
        self.display = display_surface
        self.display_rect = self.display.get_rect()
        
        self.Actors = pygame.sprite.Group()
        self.Objects = pygame.sprite.Group()
        self.map_maker = MapMaker(self.Actors, self.Objects)
        self.map_reader = Reader('content/maps/')
        
        self.start_position, image = self.map_maker.makeMap(self.map_reader.readFile('01_test.map'))
        self.setImage(image)
        self.bg_image = image.copy()


    def setImage(self, surface):
        self.image = surface
        self.rect = surface.get_rect()
        self.rect.topleft = (self.display_rect[0]/2 - self.start_position[0],\
            self.display_rect[1]/2 - self.start_position[1])
        
    def draw(self):
        self.Objects.draw(self.image)
        self.Actors.draw(self.image)
        self.display.blit(self.image, self.rect.topleft)

    def move(self, coord):
        self.image = self.bg_image.copy()
        self.rect.move_ip(coord)
    
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state.change('menu')
                    
    def loop(self):
        for sprite in self.Actors.sprites():
            sprite.loop()
        
        
class MapMaker(object):
    
    def __init__(self, actor_group, object_group):
        self.__actors = actor_group
        self.__objects = object_group

    def makeMap(self, map_id):
        start_position = map_id['start_position']
        image = loadImage(map_id['ground'])
        
        for object in map_id['objects']:
            if object['type'] == 'Actor':
                self.__actors.add(loadObject(object['type'], object))
            elif object['type'] == 'Object':
                self.__objects.add(loadObject(object['type'], object))
                
        return [start_position, image]
                
    def cleanCurrentMap(self):
        pass

@Cache()        
def loadObject(object_type, object_data):
    _fromstring = pygame.image.fromstring
    img_file = gzip.open(os.path.join(getImagePath(), \
        object_data['file']), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    if object_type == 'Object': 
        image = _fromstring(file_data['image_string'], \
            file_data['size'], file_data['format'])
        game_object = MovableObject(image, object_data['pos'], \
            file_data['collision_rect'])
    elif object_type == 'Actor':
        animations = {}
        for direction in file_data['animation']:
            animations[direction] = []
            for image_string in file_data['animation'][direction]:
                animations[direction].append(_fromstring(image_string, \
                        file_data['size'], file_data['format']))
        game_object = Actor(animations, object_data['pos'], \
            file_data['collision_rect'])
            
    return game_object