from engine.Container import LayerContainer
from actor import Actor
from engine.Decorator import Cache, Log
from engine.Object import ImmobileObject, MovableObject, AnimatedObject
from engine.Misc import loadImage, getImagePath
import pygame
from pygame.locals import *
import gzip, os.path, pickle


class World(pygame.sprite.Sprite, LayerContainer):
    
    def __init__(self, display_surface, state_handler):
        self.state = state_handler
        pygame.sprite.Sprite.__init__(self)
        LayerContainer.__init__(self, 3)
        self.display = display_surface
        self.display_rect = self.display.get_rect()
        self.map_name = ""
        self.image = None
        self.rect = None
        self.start_position = (0, 0)

    def setImage(self, surface):
        self.image = surface
        self.rect = surface.get_rect()
        self.rect.topleft = (self.display_rect[0]/2 - self.start_position[0],\
            self.display_rect[1]/2 - self.start_position[1])
        
    def draw(self):
        LayerContainer.draw(self, self.image)
        self.display.blit(self.image, self.rect.topleft)

    def move(self, coord):
        self.rect.move_ip(coord)
    
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESC:
                    self.state.change('menu')

class MapMaker(object):
    
    def __init__(self, container):
        self.__map = container
                    
        self.objects = {"Immobile": ImmobileObject,
                        "Movable": MovableObject,
                        "Animated": AnimatedObject,
                        "Actor": Actor}

    def makeMap(self, map_id):
        self.__map.start_position = map_id["start_position"]
        self.__map.setImage(pygame.transform.scale(loadImage(map_id["ground"]), (3200, 2400)))
        
        for layer in map_id["layers"]:
            ln = int(layer.replace("layer", "")) -1
            for _object in map_id["layers"][layer]:
                game_object = loadObject(self.objects[_object["type"]], _object)
                self.__map.insert(game_object, ln)

    def cleanCurrentMap(self):
        pass

@Cache()        
def loadObject(object_type, object_data):
    _fromstring = pygame.image.fromstring
    img_file = gzip.open(os.path.join(getImagePath(), \
        object_data["file"]), "rb", 1)
    file_data = pickle.load(img_file)
    img_file.close()
    if object_type != AnimatedObject: 
        image = _fromstring(file_data["image_string"], \
            file_data["size"], file_data["format"])
        game_object = object_type(image, object_data["pos"], \
            file_data["collision_rect"])
    elif object_type == Actor:
        animations = {}
        for direction in file_data["animations"]:
            animations[direction] = []
            for image_string in file_data["animations"][direction]:
                animations[direction].append(_fromstring(image_string, \
                        file_data["size"], file_data["format"]))
        game_object = object_type(animations, object_data["pos"], \
            file_data["collision_rect"])
            
    return game_object