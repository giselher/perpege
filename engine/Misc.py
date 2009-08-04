"""
@author Alexander Preisinger

Provides different tools for working with pg.
"""
import os.path, math
import pygame as pg
from Decorator import Cache
__curdir = os.path.abspath(os.path.curdir)
__IMAGE_PATH = __curdir
__SOUND_PATH = __curdir
__VIDEO_PATH = __curdir

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

def loadImage(name, colorkey=None):
    """
    Loads images.
    """
    fullname = os.path.join(__IMAGE_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        image = pg.image.load(fullname)
    except pg.error, message:
        print 'cannot load image:', name
        raise SystemExit, message
    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey is not None:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image

@Cache()
def loadSound(name):
    class NoneSound(object):
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join(__SOUND_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def loadVideo(name):
    fullname = os.path.join(__VIDEO_PATH, name)
    fullname = os.path.sep.join(fullname.split('/'))
    try:
        video = pg.movie.Movie(fullname)
    except pg.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return video

def zOrder(*groups):
    ordered = pg.sprite.OrderedUpdates()
    unordered = pg.sprite.Group(groups)
    counter = 0
    while True:
        if len(unordered) == 0: return ordered
        for sprite in unordered:
            if sprite.rect.y == counter:
                ordered.add(sprite)
                unordered.remove(sprite)
        counter += 1
        
def getDistance(point_a, point_b):
    """
    Pass 2 x-and y-coordinates to get the distance between these 2 points.
    """
    x = point_a[0]-point_b[0]
    y = point_a[1]-point_b[1]
    distance = math.sqrt(x**2 + y**2)
    return distance