from actor import Actor, Player
from reader import Reader
from engine.Decorator import Cache
from engine.Object import MovableObject
from engine.Misc import *
from engine import Input
from gui import Interface
import pygame
from pygame.locals import *
import gzip, os.path, pickle
import handler

class World(object):
    
    def __init__(self, display_surface):
        self.display = display_surface
        self.display_rect = self.display.get_rect()
        self.display_center = self.display_rect.center
        
        self.state = 'ift'
        
        self.interface = Interface(self, self.display)
        self.interface.menu.store_action('new_game', self.new_game)
        self.interface.showMenu('start')
        
        self.input = Input.I2d2axis()
        
        self.step = 10
        
        self.image = pygame.Surface((0, 0))
        self.ground = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        
        self.player = loadPlayer('Yves.ani.gz')
        
        self.deq_handler = handler.DEQ_Handler(self.player)
        
        self.Actors = []
        self.Objects = []
        self.MainGroup = pygame.sprite.Group(self.player)
        self.map_maker = MapMaker(self.MainGroup, self.Actors, self.Objects)
        self.map_reader = Reader('content/maps/')
        
        self.loops = {  'game' : self.game_loop,
                        'itf' : self.itf_loop,
                        'combat': self.combat_loop}
        
    def new_game(self):
        self.start_position, image = self.map_maker.makeMap(self.map_reader.readFile('01_test.map'))
        self.Map_init(image)
           
        self.player.events = []
        self.player.quest_events = {}
                
        self.state = 'game'

    def Map_init(self, surface):
        self.ground = surface
        self.rect = surface.get_rect()
        self.image = pygame.Surface(self.rect.size)
        self.rect.topleft = (self.display_rect.width/2-self.start_position[0],\
            self.display_rect.height/2 - self.start_position[1])
        self.player.setCenter(self.start_position)
        
    def check_collision(self, user, col_dict):
        _new = col_dict['new_crect']
        _old = col_dict['old_crect']
        self.MainGroup.remove(user)
        collide = False
        for sprite in self.MainGroup.sprites():
            if _new.colliderect(sprite.crect):
                collide = True
                
        self.MainGroup.add(user)
        if collide:
            return _old
        else:
            return _new.clamp(self.ground.get_rect())
        
    def draw(self):
        group = zOrder(self.MainGroup)
        self.image.blit(self.ground, (0, 0))
        group.draw(self.image)
        #for sprite in self.MainGroup.sprites():
        #    sprite.drawRects(self.image)
        self.display.blit(self.image, self.rect.topleft)
        group.empty()
        del group

    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.interface.showMenu()
                elif event.key == K_a: self.action()
                    
    def action(self):
        max_dist = 100
        nearest = None
        _player_center = self.player.rect.center
        self.MainGroup.remove(self.player)
        for sprite in self.MainGroup.sprites():
            _dist = getDistance(_player_center, sprite.rect.center)
            if _dist < max_dist:
                nearest = sprite
                max_dsit = _dist
         
        if nearest is not None:
            if nearest in self.Actors: 
                self.player.facing(nearest)
                nearest.facing(self.player)
                self.interface.showDialog(nearest, self.player, self.deq_handler)
                
        self.MainGroup.add(self.player)
                    
    def move(self):
        direction = self.input(self.step)
        col_dict = self.player.move(direction)

        self.player.crect = self.check_collision(self.player, col_dict)
        self.rect.x -= self.player.crect.x - col_dict['old_crect'].x
        self.rect.y -= self.player.crect.y - col_dict['old_crect'].y
        
        if direction[0] < 0:
            direction[0] = -1
        elif direction[0] > 0:
            direction[0] = 1
            
        if direction[1] < 0:
            direction[1] = -1
        elif direction[1] > 0:
            direction[1] = 1
            
        if direction[0] != 0 or direction[1] != 0:
            self.player.animate(str(direction))
            
    def game_loop(self):
        self.key_loop()
        self.move()
        for sprite in self.Actors:
            sprite.loop(self)
        self.player.loop()
        self.draw()
        
    def itf_loop(self):
        self.draw()
        self.interface.draw()
        
    def combat_loop(self):
        pass
            
    def loop(self):
        self.loops[self.state]()

        
class MapMaker(object):
    
    def __init__(self, draw_group, actor_list, object_list):
        self.__draw = draw_group
        self.__actors = actor_list
        self.__objects = object_list
        self.act_reader = Reader('content/story/actors/')

    def makeMap(self, map_id):
        start_position = map_id['start_position']
        image = loadImage(map_id['ground'])
        for _object in map_id['objects']:
            loaded_object = loadObject(_object)
            self.__objects.append(loaded_object)
            self.__draw.add(loaded_object)
        for _actor in map_id['actors']:
            loaded_object = loadActor(_actor, self.act_reader)
            self.__actors.append(loaded_object)
            self.__draw.add(loaded_object)  
                      
        return [start_position, image]
                
    def cleanCurrentMap(self):
        pass

@Cache()
def loadObject(object_data):
    img_file = gzip.open(os.path.join('content/img/', \
        object_data['file']), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    image = pygame.image.fromstring(file_data['image_string'], \
        file_data['size'], file_data['format'])
    return MovableObject(image, object_data['pos'], file_data['collision_rect'])
    
@Cache()
def loadActor(data, reader):
    actor_data = reader.readFile(data['file'])
    _fromstring = pygame.image.fromstring
    img_file = gzip.open(os.path.join('content/ani/', \
        actor_data['imageset']), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    animations = {}
    for direction in file_data['animation']:
        animations[direction] = []
        for image_string in file_data['animation'][direction]:
            animations[direction].append(_fromstring(image_string, \
                    file_data['size'], file_data['format']))
    portrait = _fromstring(file_data['portrait'], (100, 100), file_data['format'])
    return Actor(portrait, animations, data['pos'], file_data['collision_rect'], actor_data)

def loadPlayer(file):
    _fromstring = pygame.image.fromstring
    img_file = gzip.open(os.path.join('content/ani/', file), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    animations = {}
    for direction in file_data['animation']:
        animations[direction] = []
        for image_string in file_data['animation'][direction]:
            animations[direction].append(_fromstring(image_string, \
                    file_data['size'], file_data['format']))
    portrait = _fromstring(file_data['portrait'], (100, 100), file_data['format'])
    return Player(portrait, animations, (0, 0), file_data['collision_rect'])