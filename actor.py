import pygame
from engine.Object import MovableObject
from saas import SaAS


class Actor(MovableObject, SaAS):

    def __init__(self, portrait, animations, \
            position, col_rect, actor_data=None):

        MovableObject.__init__(self, animations['down'][3], position, col_rect)
        SaAS.__init__(self)

        self.is_player = False

        self.portrait = portrait

        if actor_data is not None:
            self.name = actor_data['name']
            self.dialogs = actor_data['dialogs']

        self.id = actor_data

        self.diff_x = self.crect.x - self.rect.x
        self.diff_y = self.crect.y - self.rect.y

        self.animations = animations
        self.directions = { 'up' : [0, -1],
                            'down' : [0, 1],
                            'left' : [-1, 0],
                            'right' : [1, 0],
                            'none' : [0, 0]}
       #temporarly
        self.step = 5
        self.a_step = 0
        self.i_step = 0

        self.prev_dir = 'none'

#    def clamp(self, rect):
#        self.rect.clamp_ip(rect)
#        self.crect.topleft = \
#            (self.rect.x+self.diff_x, self.rect.y+self.diff_y)

    def action(self, target):
        pass

    def facing(self, target):
        if target.crect.center[0] < self.crect.center[0]:
            if target.crect.center[1] < self.crect.center[1]:
                if (self.crect.center[0] - target.crect.center[0]) < \
                        (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['left'][3]
            else:
                if (self.crect.center[0] - target.crect.center[0]) < \
                        (target.crect.center[1] - self.crect.center[1]):
                    self.image = self.animations['down'][3]
                else:
                    self.image = self.animations['left'][3]
        else:
            if target.crect.center[1] < self.crect.center[1]:
                if (target.crect.center[0] - self.crect.center[0]) < \
                        (self.crect.center[1] - target.crect.center[1]):
                    self.image = self.animations['up'][3]
                else:
                    self.image = self.animations['right'][3]
            else:
                if (target.crect.center[0] - self.crect.center[0]) < \
                        (target.crect.center[1] - self.crect.center[1]):
                    self.image = self.animations['down'][3]
                else:
                    self.image = self.animations['right'][3]

    def face(self, direction):
        self.image = self.animations[direction][3]

    def animate(self, direction):
        """
        up, down, left, right, ...
        """
        if direction == self.prev_dir:
            if self.a_step == 1:
                self.i_step += 1
                self.a_step = 0
            else:
                self.a_step += 1
        else:
            self.a_step = 0
            self.i_step = 0
            self.prev_dir = direction
        try:
            self.image = self.animations[direction][self.i_step]
        except IndexError:
            self.i_step = 0

    def set_center(self, coord):
        self.rect.center = coord
        self.crect.topleft = (self.rect.x+self.diff_x, self.rect.y+self.diff_y)

    def move(self, coord):
        crect = self.crect.move(coord)
        # return old, new
        return crect, self.crect

    def loop(self, world):
        _choice = self.prev_dir
        direction = self.directions[_choice]
        direction = [direction[0]*self.step, direction[1]*self.step]

        # The same as in the cls.move, but its faster
        # without an extra function call.

        self.set_center(world.clamp(self.rect).center)

        crect = self.crect.move(direction)

        self.crect = world.check_collision(self, crect, self.crect)

        self.rect.topleft = \
            (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

        self


class Player(Actor):

    def __init__(self, portrait, animations, position, col_rect):
        Actor.__init__(self, portrait, animations, position, col_rect)
        self.world = None

        self.name = "Yves"

        self.is_player = True

        self.events = []
        self.quest_events = {}

        # Will work on a better solution
        self.directions = { '[0, -1]' :  'up',
                            '[0, 1]' : 'down',
                            '[-1, 0]' : 'left',
                            '[1, 0]' : 'right',
                            '[1, 1]' : 'downright',
                            '[-1, 1]' : 'downleft',
                            '[1, -1]' : 'upright',
                            '[-1, -1]' : 'upleft'}

    def animate(self, direction):
        Actor.animate(self, self.directions[direction])

    def loop(self):
        self.rect.topleft = \
            (self.crect.x-self.diff_x, self.crect.y-self.diff_y)

        self.set_center(self.world.clamp(self.rect).center)