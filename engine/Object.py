"""
@author Alexander Preisnger

Provides Objects classes wich inherits form Sprite classes.

Object (inherit from pygame.sprite.Sprite)
    - attributes
        + crect (for collision detection)
    - methods
        + drawRects (draws the rect and crect)
        + setPosition (sets the position of the rect and crect)
        + setCollisionRect (change or set the crect)
        
ImmobileObject (inherit from Object)
    
MovableObject (inherit form Object)
    - methods
        + move (moves the rect and the crect)
        
AnimatedObject (inherit form MovableObject)
    - methods
        + setAnimations (sets the animations)
        + loop (animation loop)
        
"""

from pygame import Sprite, Surface
from pygame import draw as _draw

class Object(Sprite):
    
    def __init__(self, surface, position, collision_rect):
        """
        The same as ImmobileObject
        """
        Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        
        self.crect = (collision_rect if not collision_rect is None \
            else self.image.get_rect())
       
        self.__crect_rel_x = self.crect.x
        self.__crect_rel_y = self.crect.y
        
        self.rect.topleft = position
        self.crect.topleft = (self.rect.x+self.__crect_rel_y, self.rect.y+self.__crect_rel_y)
    
    def drawRects(self, surface):
        """
        Draws the contours of the collision rect and the image rect.
        Usefuf for debuging.
        """
        _draw.rect(surface, (0, 0, 0), self.rect, 2)
        _draw.rect(surface, (200, 50, 200), self.crect, 2)
        
    def setPosition(self, position):
        """(x, y)
        Set the position for the rect and the crect.
        """
        self.rect.topleft = position
        self.crect.topleft = (position[0]+self.__crect_rel_x, position[1]+self.__crect_rel_y)
        
    def setCollisionRect(self, rect):
        """
        Set the crect.
        
        The x and y coordinate must be relative to the rect.
        """
        self.crect = rect
        
        self.__crect_rel_x = self.crect.x
        self.__crect_rel_y = self.crect.y
        
        self.crect.topleft = (self.rect.x+self.__crect_rel_y, self.rect.y+self.__crect_rel_y)

class ImmobileObject(Object):
    
    def __init__(self, surface, position=(0, 0), collision_rect=None): 
        """
        Inherits form pygame.sprite.Sprite and provides
        a collisioin Rect (crect) for precis collison
        detection.
        
        If the collision_rect is None then it's the same as 
        the image rect.The position of the collision rect is 
        relative to the postion of the image rect.

        """
        Object.__init__(self, surface, position, collision_rect)
        
class MovableObject(Object):
    
    def __init__(self, surface, position, collision_rect=None):
        """
        Inherits form pygame.sprite.Sprite and provides
        a collisioin Rect (crect) for precis collison
        detection.
        
        If the collision_rect is None then it's the same as 
        the image rect.The position of the collision rect is 
        relative to the postion of the image rect.
       
        If center is givent the image center will be set at 
        given position.
        """
        Object.__init__(self, surface, position, collision_rect)
        
    def move(self, direction):
        """(x, y)
        Moves the object.
        """
        self.rect.move_ip(direction)
        self.crect.move_ip(direction)
        
class AnimatedObject(MovableObject):
    
    def __init__(self, animations=[], position=(0, 0), collision_rect=None):
        """
        
        Inherits form MovableObject and provides
        a collisioin Rect (crect) for precis collison
        detection.
        
        If the collision_rect is None then it's the same as 
        the image rect.The position of the collision rect is 
        relative to the postion of the image rect.
       
        If center is givent the image center will be set at 
        given position.
        """
        image = (animations[0] if len(animations) > 0 else Surface((0, 0)))
            
        MovableObject.__init__(image, position, collision_rect)
        
        self.__animations = animations
        self.__max_count = len(animations)-1
        self.__counter = 0
    
    def setAnimations(self, animations):
        """
        Pass a list with surfaces for the animation loop.
        
        I didn't test it yet but i looks like it would not work
        """
        self.image = animations[0]
        self.rect = self.image.get_rect()
        self.crect = self.rect
        self.__animations = animations
        self.__max_count = len(animations)-1
        
    def loop(self):
        """
        Every call it changes the image.
        """
        if self.__counter == self.__max_count: self.__counter = 0
        self.image = self.__animations[self.__counter]
        self.__counter += 1
        