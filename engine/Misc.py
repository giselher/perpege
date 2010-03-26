"""
@author Alexander Preisinger

Provides different tools for working with pygame.
"""
import math
import os.path
import pygame
from Decorator import Cache

__curdir = os.path.abspath(os.path.curdir)
__IMAGE_PATH = __curdir
__SOUND_PATH = __curdir
__VIDEO_PATH = __curdir

def setAllPaths(path):
    """\
    Set the image, sound and video path at once.
    """
    global __IMAGE_PATH, __SOUND_PATH, __VIDEO_PATH
    __IMAGE_PATH, __SOUND_PATH, __VIDEO_PATH = path

def setImagePath(path):
    global __IMAGE_PATH
    __IMAGE_PATH = path

def setSoundPath(path):
    global __SOUND_PATH
    __SOUND_PATH = path

def setVideoPath(path):
    global __VIDEO_PATH
    __VIDEO_PATH = path

def getImagePath():
    global __IMAGE_PATH
    return __IMAGE_PATH

def getSoundPath():
    global __SOUND_PATH
    return __SOUND_PATH

def getVideoPath():
    global __VIDEO_PATH
    return __VIDEO_PATH

@Cache()
def loadImage(name, colorkey=None):
    """
    Loads images.
    """
    fullname = os.path.join(__IMAGE_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'cannot load image:', name
        raise SystemExit, message
    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey is not None:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

@Cache()
def loadSound(name):
    class NoneSound(object):
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(__SOUND_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def loadVideo(name):
    fullname = os.path.join(__VIDEO_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        video = pygame.movie.Movie(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return video

def zOrder(*groups):
    ordered = pygame.sprite.OrderedUpdates()
    sprites = pygame.sprite.Group(groups)

    counter = 0
    while len(sprites.sprites()):

        for sprite in sprites.sprites():
            if sprite.rect.y + sprite.rect.height == counter:
                ordered.add(sprite)
                sprites.remove(sprite)

        counter += 1

    return ordered

def getDistance(point_a, point_b):
    """
    Pass 2 x-and y-coordinates to get the distance between these 2 points.
    """
    x = point_a[0]-point_b[0]
    y = point_a[1]-point_b[1]
    distance = math.sqrt(x**2 + y**2)
    return distance