from actor import Actor, Player
from reader import Reader
from engine.Decorator import Cache
from engine.Object import MovableObject
from engine.Misc import loadImage, getImagePath, zOrder
from engine import Input
import pygame
from pygame.locals import *
import gzip, os.path, pickle

class World(object):
    
    def __init__(self, display_surface, state_handler):
        self.state = state_handler
        self.display = display_surface
        self.display_rect = self.display.get_rect()
        self.display_center = self.display_rect.center
        self.input = Input.I2d4axis()
        
        self.step = 10
        
        self.ground = None
        self.image = None
        self.rect = None
        
        self.player = loadObject({'type': 'Player', 'pos' : (self.display_rect.width/2, \
            self.display_rect.height/2) ,'file' : 'ani/Dummy.ani.gz'})
        
        self.Actors = [self.player]
        self.Objects = []
        self.DrawGroup = pygame.sprite.Group(self.player)
        self.map_maker = MapMaker(self.DrawGroup, self.Actors, self.Objects)
        self.map_reader = Reader('content/maps/')
        
        self.start_position, image = self.map_maker.makeMap(self.map_reader.readFile('01_test.map'))
        self.setImage(image)
        
        self.directions = { '[0, -1]' :  'up',
                            '[0, 1]' : 'down',
                            '[-1, 0]' : 'left',
                            '[1, 0]' : 'right',
                            '[1, 1]' : 'downright',
                            '[-1, 1]' : 'downleft',
                            '[1, -1]' : 'upright',
                            '[-1, -1]' : 'upleft'}

    def setImage(self, surface):
        self.ground = surface
        self.rect = surface.get_rect()
        self.image = pygame.Surface(self.rect.size)
        self.rect.topleft = (self.display_rect.width/2-self.start_position[0],\
            self.display_rect.height/2 - self.start_position[1])
        self.player.setPosition(self.start_position)
        
    def draw(self):
        self.image.blit(self.ground, (0, 0))
        zOrder(self.DrawGroup).draw(self.image)
        for sprite in self.DrawGroup.sprites():
            sprite.drawRects(self.image)
        self.display.blit(self.image, self.rect.topleft)

    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state.change('menu')
                    
    def move(self):
        direction = self.input(-self.step)
        _direction = [direction[0]*-1,direction[1]*-1]
        self.player.move(_direction)
        self.player.clamp(self.ground.get_rect())
        self.rect.move_ip(direction)
        if direction[0] < 0:
            direction[0] = 1
        elif direction[0] > 0:
            direction[0] = -1
            
        if direction[1] < 0:
            direction[1] = 1
        elif direction[1] > 0:
            direction[1] = -1
            
        if not (direction[0] == 0 and direction[1] == 0):
            self.player.animate(self.directions[str(direction)])
                    
    def loop(self):
        self.key_loop()
        self.move()
        for sprite in self.Actors:
            sprite.loop()
            sprite.clamp(self.ground.get_rect())

        self.draw()
        
class MapMaker(object):
    
    def __init__(self, draw_group, actor_list, object_list):
        self.__draw = draw_group
        self.__actors = actor_list
        self.__objects = object_list

    def makeMap(self, map_id):
        start_position = map_id['start_position']
        image = loadImage(map_id['ground'])
        for _object in map_id['objects']:
            loaded_object = loadObject(_object)
            if _object['type'] == 'Actor':
                self.__actors.append(loaded_object)
            elif _object['type'] == 'Object':
                self.__objects.append(loaded_object)
            self.__draw.add(loaded_object)
        return [start_position, image]
                
    def cleanCurrentMap(self):
        pass

@Cache()        
def loadObject(object_data):
    _fromstring = pygame.image.fromstring
    img_file = gzip.open(os.path.join(getImagePath(), \
        object_data['file']), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    animations = {}
    if object_data['type'] == 'Object': 
        image = _fromstring(file_data['image_string'], \
            file_data['size'], file_data['format'])
        game_object = MovableObject(image, object_data['pos'], \
            file_data['collision_rect'])
    
    elif object_data['type'] == 'Actor':
        for direction in file_data['animation']:
            animations[direction] = []
            for image_string in file_data['animation'][direction]:
                animations[direction].append(_fromstring(image_string, \
                        file_data['size'], file_data['format']))
        game_object = Actor(animations, object_data['pos'], \
            file_data['collision_rect'])
            
    elif object_data['type'] == 'Player':
        for direction in file_data['animation']:
            animations[direction] = []
            for image_string in file_data['animation'][direction]:
                animations[direction].append(_fromstring(image_string, \
                        file_data['size'], file_data['format']))
        game_object = Player(animations, object_data['pos'], \
            file_data['collision_rect'])
    
    return game_object