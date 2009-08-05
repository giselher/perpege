
import pygame
import math, sys
import gettext
from pygame.locals import *
_ = gettext.gettext
sys.path.append('../')
import engine

class MenuButton(pygame.sprite.Sprite):
    
    def __init__(self, parent, name, text, position):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = name
        
        self.font = pygame.font.Font('content/tahoma.ttf', 24)
        self.image = self.font.render(text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        
        self.rect.center = position
        self.y = position[1]
        
        self.function = None
        
    def hover(self):
        self.image = pygame.transform.scale(self.image, (self.rect.width*2, self.rect.height*2))
        self.rect = self.image.get_rect()
        self.rect.center = (self.parent.rect.width/2, self.y)
        
    def normal(self):
        self.image = pygame.transform.scale(self.image, (self.rect.width/2, self.rect.height/2))
        self.rect = self.image.get_rect()
        self.rect.center = (self.parent.rect.width/2, self.y)
        
    def action(self):
        if self.function is not None:
            self.function()

    def store_action(self, function):
        self.function = function

class MainMenu(pygame.sprite.Sprite):
    
    def __init__(self, screen, bg_image_path=None):
        pygame.sprite.Sprite.__init__(self)
        self.__group = pygame.sprite.Group()
        self.loadImage = engine.Misc.loadImage
        self.screen = screen
        
        self.sel_button = 0

        if bg_image_path is None:
            self.image = self.loadImage('menu.png')
        else:
            self.image = self.loadImage(bg_image_path)
            
        self.rect = self.image.get_rect()

        self.buttons = [MenuButton(self, 'new_game', _("New Game"), (self.rect.width/2, 150)),
            MenuButton(self, 'loag_game', _("Load Game"), (self.rect.width/2, 250)),
            MenuButton(self, 'save_game', _("Save Game"), (self.rect.width/2, 350)),
            MenuButton(self, 'quit', _("Quit"), (self.rect.width/2, 450)),]
                  
        self.buttons[self.sel_button].hover()
        
    def store_action(self, button_name, function):
        for button in self.buttons:
            if button.name == button_name:
                button.store_action(function)

    def draw(self):
        for button in self.buttons:
            self.__group.add(button)
        self.screen.blit(self.image, (0, 0))
        self.__group.draw(self.screen)
        self.__group.empty()
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN: self.key_down()
                elif event.key == K_UP: self.key_up()
                elif event.key == K_RETURN: self.key_return()
            
    def key_down(self):
        self.buttons[self.sel_button].normal()
        if not self.sel_button == 3: self.sel_button += 1
        else: self.sel_button = 0
        self.buttons[self.sel_button].hover()
    
    def key_up(self):
        self.buttons[self.sel_button].normal()
        if not self.sel_button == 0: self.sel_button -= 1
        else: self.sel_button = 3
        self.buttons[self.sel_button].hover()
        
    def key_return(self):
        self.buttons[self.sel_button].action()