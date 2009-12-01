import os.path
import pickle
import gzip
import pygame
import gss
import handler
from actor import Actor, Player
from reader import Reader
from engine.Object import MovableObject
from engine.Misc import *
from engine import Input
from gui import Interface
from combat import Combat
from pygame.locals import *

class World(object):
    
    def __init__(self, display_surface, settings):
        self.display = display_surface
        self.display_rect = self.display.get_rect()
        self.display_center = self.display_rect.center
        
        self.settings = settings
        self.key_map = settings.get_key_map()
        
        self.delayed_functions = []
        
        self.state = 'ift'
        self.prev_state = 'game'
        
        self.Saver = gss.Saver('./saves/')
        self.Loader = gss.Loader('./saves/')
        
        self.interface = Interface(self, self.display)
        self.interface.menu.store_action('new_game', self.new_game)
        self.interface.menu.store_action('load_game', self.load_game)
        self.interface.menu.store_action('save_game', self.save_game)
        self.interface.showMenu('start')
        
        self.combat = Combat(self, self.display, self.interface)
        
        self.input = Input.I2d2axis(self.key_map)
        
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
                
        self.loops = {  'game' : self.game_loop,
                        'itf' : self.itf_loop,
                        'combat': self.combat_loop}
        
    def new_game(self):
        self.initMap('01_test.map.xml')
           
        self.player.prev_dir = 'down'
        self.player.image = self.player.animations['down'][3]
        self.player.events = []
        self.player.quest_events = {}
                
        self.state = 'game'
        
    def save_game(self, filename):
        self.Saver.prepare(self.map_maker.map_filename, 'map_filename')
        self.Saver.prepare(self.player.events, 'events')
        self.Saver.prepare(self.player.quest_events, 'quest_events')
        self.Saver.prepare(self.player.rect.center, 'position')
        self.Saver.prepare(self.player.animations[ \
            self.player.prev_dir].index(self.player.image), 'image_id')
        self.Saver.prepare(self.player.prev_dir, 'previous_direction')
        self.Saver.save(filename)
        
        self.state = 'game'
        
    def load_game(self, filename):
        self.Loader.load(filename)
        
        self.player.events = self.Loader.get('events')
        self.player.quest_events = self.Loader.get('quest_events')
        self.player.prev_dir = self.Loader.get('previous_direction')
        self.player.image = self.player.animations[self.player.prev_dir] \
            [self.Loader.get('image_id')]
             
        self.initMap(self.Loader.get('map_filename'), self.Loader.get('position'))
               
        self.state = 'game'
        
    def initMap(self, map_name, position=None):
        self.map_maker.makeMap(map_name)
        
        if position: self.map_maker.start_position = position
        
        self.ground = self.map_maker.ground_image
        self.rect = self.ground.get_rect()
        self.image = pygame.Surface(self.rect.size)
        self.rect.topleft = (self.display_rect.width/2-self.map_maker.start_position[0],\
            self.display_rect.height/2 - self.map_maker.start_position[1])
        self.player.setCenter(self.map_maker.start_position)
        
        self.combat.initMap(self.ground)

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
        
    def add_delayed_function(self, function):
        """Store a function to be called in the next main loop."""
        self.delayed_functions.append(function)
        
    def draw(self):
        group = zOrder(self.MainGroup)
        self.image.blit(self.ground, (0, 0))
        group.draw(self.image)
        #for sprite in self.MainGroup.sprites():
        #    sprite.drawRects(self.image)
        self.display.blit(self.image, self.rect.topleft)
        group.empty()

    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.interface.showMenu()
                elif event.key == self.key_map['action']: self.action()
                elif event.key == K_f: 
                    for actor in self.Actors:
                        if actor.name == "Duster":
                            self.prev_state = "game"
                            self.combat.Fight(self.player, [actor])
                    
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
                self.interface.showDialog(nearest, \
                    self.player, self.deq_handler)
                
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
        self.combat.loop()
        self.combat.draw()
        
    def loop(self):
        if len(self.delayed_functions) > 0:
            for func in self.delayed_functions:
                self.delayed_functions.remove(func)
                func()
                
        self.loops[self.state]()

        
class MapMaker(object):
    
    def __init__(self, draw_group, actor_list, object_list):
        self.__draw = draw_group
        self.__actors = actor_list
        self.__objects = object_list
        self.map_reader = Reader('content/maps/')
        self.act_reader = Reader('content/story/actors/')
        
        self.start_position = (0, 0)
        self.ground_image = None
        self.map_name = None
        self.map_filename = ''
        
    def makeMap(self, map_name):
        map_id = self.map_reader.readMapFile(map_name)
        self.start_position = map_id['start_position']
        self.ground_image = loadImage(map_id['ground'])
        self.map_name = map_id['name']
        self.map_filename = map_id['filename']
        for _object in map_id['objects']:
            loaded_object = loadObject(_object)
            self.__objects.append(loaded_object)
            self.__draw.add(loaded_object)
        for _actor in map_id['actors']:
            loaded_object = loadActor(_actor, self.act_reader)
            self.__actors.append(loaded_object)
            self.__draw.add(loaded_object)  
                
    def cleanCurrentMap(self):
        pass
        
#class InputNew(object):
#    
#    def __init__(self):
#        pass
#        

@Cache()    
def loadObject(object_data):
    # object_data[0] ... filename
    # object_data[1] ... position
    img_file = gzip.open(os.path.join('content/img/', \
        object_data[0]), 'rb', 1)
    file_data = pickle.load(img_file)
    img_file.close()
    image = pygame.image.fromstring(file_data['image_string'], \
        file_data['size'], file_data['format'])
    return MovableObject(image, object_data[1], file_data['collision_rect'])
    
@Cache()
def loadActor(data, reader):
    # data[0] ... filename
    # data[1] ... position
    actor_data = reader.readActFile(data[0])
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
    return Actor(portrait, animations, data[1], file_data['collision_rect'], actor_data)

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