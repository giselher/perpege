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

img_filename = raw_input("-->")
path = os.path.join(_curdir, img_filename)
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

r = os.listdir(os.path.join(_curdir, "r"))
l = os.listdir(os.path.join(_curdir, "l"))
d = os.listdir(os.path.join(_curdir, "d"))
u = os.listdir(os.path.join(_curdir, "u"))
dr = os.listdir(os.path.join(_curdir, "dr"))
dl = os.listdir(os.path.join(_curdir, "dl"))
ul = os.listdir(os.path.join(_curdir, "ul"))
ur = os.listdir(os.path.join(_curdir, "ur"))

pygame.display.init()
pygame.display.set_mode((1,1))

for name in r:
    image = load_image(os.path.join("r", name))
    ani_data["animation"]["right"].append(pygame.image.tostring(image, img_data["format"]))

for name in l:
    image = load_image(os.path.join("l", name))
    ani_data["animation"]["left"].append(pygame.image.tostring(image, img_data["format"]))
    
for name in d:
    image = load_image(os.path.join("d", name))
    ani_data["animation"]["down"].append(pygame.image.tostring(image, img_data["format"]))
    
for name in u:
    image = load_image(os.path.join("u", name))
    ani_data["animation"]["up"].append(pygame.image.tostring(image, img_data["format"]))

for name in dr:
    image = load_image(os.path.join("dr", name))
    ani_data["animation"]["downright"].append(pygame.image.tostring(image, img_data["format"]))

for name in dl:
    image = load_image(os.path.join("dl", name))
    ani_data["animation"]["downleft"].append(pygame.image.tostring(image, img_data["format"]))
    
for name in ul:
    image = load_image(os.path.join("ul", name))
    ani_data["animation"]["upleft"].append(pygame.image.tostring(image, img_data["format"]))
    
for name in ur:
    image = load_image(os.path.join("ur", name))
    ani_data["animation"]["upright"].append(pygame.image.tostring(image, img_data["format"]))

ani_data["image_string"] = ani_data["animation"]["down"][0]    
ani_data["portrait"] = pygame.image.tostring(load_image("portrait.png"), img_data["format"])
    
    
ani_file = gzip.open(img_filename.split(".")[0]+".ani.gz", "wb", 1)
pickle.dump(ani_data, ani_file, 1)
ani_file.close()
print "succes"
