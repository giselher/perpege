
import pygame, math, gettext
from pygame.locals import *
from __init__ import loadImage

_ = gettext.gettext


class MenuButton(pygame.sprite.Sprite):
    
    def __init__(self, parent, name, text, position):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = name
        
        self.font = pygame.font.Font('content/tahoma.ttf', 24)
        self.image = self.font.render(text, True, (255, 255, 255))
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

class MainMenu(object):
    
    def __init__(self, state_handler, bg_image_path=None):
        self.state = state_handler
        self.__group = pygame.sprite.Group()
        self.loadImage = loadImage
        
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
        
        for button in self.buttons:
            self.__group.add(button)
        
    def store_action(self, button_name, function):
        for button in self.buttons:
            if button.name == button_name:
                button.store_action(function)

    def draw(self, surface):
        self.key_loop()
        surface.blit(self.image, (0, 0))
        self.__group.draw(surface)
        
    def resume(self):
        if self.state.previous is not None:
            self.state.change(self.state.previous)
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN: self.key_down()
                elif event.key == K_UP: self.key_up()
                elif event.key == K_RETURN: self.key_return()
                elif event.key == K_ESCAPE: self.resume()
            
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