#!/usr/bin/env python

import pygame, sys, os, pickle, gzip
from pygame.locals import *
import Object
pygame.init()

FORMAT = "RGBA"
DATA = None
WORK_OBJECT = None
BCOLOR = (100, 100, 100)
SCREEN_SIZE = (400, 480)
GROUP = pygame.sprite.Group()


def load_image(name, colorkey=None):
    """
    Loads images.
    """
    fullname = os.path.join(os.path.abspath(os.path.curdir), name)
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

class Widget(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
    def render(self, text):
        return self.font.render(self.text, True, (255, 255, 255))

class Button(Widget):
    
    def __init__(self, text, color, size, pos, func):
        Widget.__init__(self)
        self.do = func
        self.text = text
        self.color = color
        self.pressed = False
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.font = pygame.font.SysFont("monospace", 16)
        self.font_render = self.render(self.text)
        self.font_rect = self.font_render.get_rect()
        self.image.blit(self.font_render, (self.rect.width/2-self.font_rect.width/2,\
            self.rect.height/2-self.font_rect.height/2))
    
    def hover(self, hover):
        if hover: self.image.fill((200, 200, 200))
        else: self.image.fill(self.color)
        self.image.blit(self.font_render, (self.rect.width/2-self.font_rect.width/2,\
            self.rect.height/2-self.font_rect.height/2))      
            
class Bar(Widget):
    
    def __init__(self, color, size, pos):
        Widget.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.font = pygame.font.SysFont("monospace", 12)
        self.input_bar = pygame.Surface((size[0]-size[1], size[1]/2))
        self.input_bar.fill(color)
        bar_rect = self.input_bar.get_rect()
        self.bar_pos = (size[0]/2-bar_rect.width/2, size[1]/2-bar_rect.height/2)
        self.image.blit(self.input_bar, self.bar_pos)
        self.text = os.path.curdir+os.sep
        self.reDrawText(self.text)
        
    def reDrawText(self, text):
        text_r = self.render(text)
        pos_t = (self.bar_pos[0]+1, self.bar_pos[1]+3)
        self.image.blit(self.input_bar, self.bar_pos)
        self.image.blit(self.render(text), pos_t)
        
    def keyloop(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.Backspace()
        elif event.key == pygame.K_RETURN:
            pass
        else:
            self.text += event.unicode
            self.reDrawText(self.text)
            
    def Backspace(self):
            self.text = self.text[0:-1]
            self.reDrawText(self.text)
            
InputBar = Bar(BCOLOR, (SCREEN_SIZE[0], 40), (0, 0))
GROUP.add(InputBar)

def save():
    if not WORK_OBJECT is None:
        _ = WORK_OBJECT
        col_rect = pygame.Rect((_.crect.x -_.rect.x, _.crect.y - _.rect.y), _.crect.size)
        if DATA is None:
            image_data = {"image_string" : pygame.image.tostring(_.image, FORMAT),
                          "format" : FORMAT,
                          "size" : _.rect.size,
                          "collision_rect": col_rect}
        else:
            image_data = DATA
            image_data["collision_rect"] = col_rect
        img_file = gzip.open(InputBar.text, "wb", 1)
        pickle.dump(image_data, img_file, 1)
        print "image saved"
        img_file.close()

        

def clear():
    if not WORK_OBJECT is None:
        WORK_OBJECT.crect = pygame.Rect(0, 0, 0, 0)
            
def quit():
    print("Application closed")
    pygame.quit()
    sys.exit(0)

def load():
    global WORK_OBJECT, DATA
    _img_name = InputBar.text
    if os.path.exists(_img_name):
        if _img_name.endswith(".img.gz") or _img_name.endswith(".ani.gz"):
            img_file = gzip.open(InputBar.text, "rb", 1)
            data = pickle.load(img_file)
            img_file.close()
            image = pygame.image.fromstring(data["image_string"], data["size"], data["format"])
            CollObject = Object.ImmobileObject(image, collision_rect=data["collision_rect"])
            DATA = data
        else:
            image = load_image(_img_name)
            CollObject = Object.ImmobileObject(image, collision_rect=pygame.Rect(0, 0, 0, 0))     
            DATA = None
        
        rect = image.get_rect()
        CENTER_POS = (SCREEN_SIZE[0]/2-rect.width/2, SCREEN_SIZE[1]/2-rect.height/2)
        CollObject.setPosition(CENTER_POS)
        for sprite in GROUP:
            if not sprite is InputBar:
                GROUP.remove(sprite)
        GROUP.add(CollObject)
        WORK_OBJECT = CollObject
    else:
        print "file doesn't exist"

def main(): 
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Collision Rect Setter")
    
    BCOLOR = (100, 100, 100)
    BSIZE = (SCREEN_SIZE[0]/4, 40)
    DOWN = SCREEN_SIZE[1]-BSIZE[1]
    ButtonGroup = pygame.sprite.Group([Button("Load", BCOLOR, BSIZE, (0, DOWN), load), \
        Button("Save", BCOLOR, BSIZE, (BSIZE[0], DOWN), save), \
        Button("Clear Rect", BCOLOR, BSIZE, (BSIZE[0]*2, DOWN), clear), \
        Button("Close", BCOLOR, BSIZE, (BSIZE[0]*3, DOWN), quit)])


    background = pygame.surface.Surface((800, 600))
    background.fill((255, 255, 255))
    pressed = None
    prev_pos = None
    RESIZE = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                InputBar.keyloop(event)
 
        mouse_pos = pygame.mouse.get_pos()
        for button in ButtonGroup:
            if button.rect.collidepoint(mouse_pos):
                button.hover(True)  
                if pygame.mouse.get_pressed()[0]:
                    pressed = button
                else:
                    if button is pressed:
                        button.do()
                        pressed = None
            else:
                button.hover(False)
        
        screen.blit(background, (0,0))
        ButtonGroup.draw(screen)
        GROUP.draw(screen)
        if not WORK_OBJECT is None: 
            WORK_OBJECT.drawRects(screen)
            
            if WORK_OBJECT.crect.collidepoint(mouse_pos) and not RESIZE:
                if pygame.mouse.get_pressed()[0]:
                    if prev_pos is None:
                        prev_pos = mouse_pos
                    else:
                        y_diff = mouse_pos[1] - prev_pos[1]
                        x_diff = mouse_pos[0] - prev_pos[0]
                        WORK_OBJECT.crect.x += x_diff
                        WORK_OBJECT.crect.y += y_diff
                        prev_pos = mouse_pos
                        WORK_OBJECT.crect.clamp_ip(WORK_OBJECT.rect)
                        
            elif WORK_OBJECT.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    if WORK_OBJECT.crect.x == 0:
                        WORK_OBJECT.crect.topleft = mouse_pos
                        
                    else:
                        if mouse_pos[0] <= WORK_OBJECT.crect.x:
                            width = WORK_OBJECT.crect.x - mouse_pos[0]
                            WORK_OBJECT.crect.x = mouse_pos[0]
                            b = WORK_OBJECT.crect.w
                            WORK_OBJECT.crect.width += width 
                            print "x:",WORK_OBJECT.crect.x, b, width, WORK_OBJECT.crect.w
                        else:
                            WORK_OBJECT.crect.width = mouse_pos[0] - WORK_OBJECT.crect.x
                            
                        if mouse_pos[1] <= WORK_OBJECT.crect.y:
                            height = WORK_OBJECT.crect.y - mouse_pos[1]
                            WORK_OBJECT.crect.y = mouse_pos[1] 
                            b = WORK_OBJECT.crect.height
                            WORK_OBJECT.crect.height += height 
                            print "y:", WORK_OBJECT.crect.y, b, height, WORK_OBJECT.crect.h
                        else:
                            WORK_OBJECT.crect.h = mouse_pos[1] - WORK_OBJECT.crect.y
                        print WORK_OBJECT.crect
                    RESIZE = True

                else:
                    prev_pos = None
                    RESIZE = False
                                                
        pygame.display.flip()
    
if __name__ == "__main__":
    main()