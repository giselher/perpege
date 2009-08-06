#!/usr/bin/env python

import pygame, sys, os, pickle, gzip
_curdir = os.path.curdir

def load_image(name, colorkey=None):
    """
    Loads images.
    """
    fullname = os.path.join(os.path.abspath(_curdir), name)
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
if len(sys.argv) == 1:
    print 'please pass a filename'
    sys.exit()
path = sys.argv[1]
if os.path.exists(path): img_file = gzip.open(path)
else:
    print "file doesn't exist"
    sys.exit()

img_data = pickle.load(img_file)

ani_data = {"format": img_data["format"],
            "size" : img_data["size"],
            "collision_rect": img_data["collision_rect"],
            "animation": {
                "right" : [],
                "left" : [],
                "down" : [],
                "up" : [],
                "downright" : [],
                "upleft" : [],
                "downleft" : [],
                "upright" : [],
                }
            }


pygame.display.init()
pygame.display.set_mode((1,1))

def add_animation(directory, direction):
        _cur = os.listdir(os.path.join(_curdir, directory))
        for name in _cur:
            if not name.startswith("."):
                image = load_image(os.path.join(directory, name))
                ani_data["animation"][direction].append(pygame.image.tostring(image, img_data["format"]))
                
add_animation('r', 'right')
add_animation('l', 'left')
add_animation('u', 'up')
add_animation('d', 'down')
add_animation('dl', 'downleft')
add_animation('dr', 'downright')
add_animation('ur', 'upright')
add_animation('ul', 'upleft')

ani_data["image_string"] = ani_data["animation"]["down"][0]    
ani_data["portrait"] = pygame.image.tostring(load_image("portrait.png"), img_data["format"])
    
    
ani_file = gzip.open(path.split(".")[0]+".ani.gz", "wb", 1)
pickle.dump(ani_data, ani_file, 1)
ani_file.close()
print "succes"
