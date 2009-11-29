import os.path
import pygame
import gettext
from pygame.locals import *

_ = gettext.gettext

class MenuButton(pygame.sprite.Sprite):
    
    def __init__(self, parent, name, text, position, align):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.name = name
        
        self.align = align
        self.position = position
        self.text = text
        
        self.active = True
        
        self.font = pygame.font.Font('content/tahoma.ttf', 24)
        self.image = self.render(text)
        self.rect = self.image.get_rect()
        
        exec('self.rect.%s = %s' % (align, position))
        
        self.function = None
        
    def render(self, text):
        return self.font.render(text, True, (255, 255, 255))
        
    def hover(self):
        self.image = pygame.transform.scale(self.image, 
            (self.rect.width * 2, self.rect.height * 2))
        self.rect = self.image.get_rect()
        exec('self.rect.%s = %s' % (self.align, str(self.position)))
        
    def normal(self):
        self.image = pygame.transform.scale(self.image, 
            (self.rect.width / 2, self.rect.height / 2))
        self.rect = self.image.get_rect()
        exec('self.rect.%s = %s' % (self.align, str(self.position)))
        
    def action(self):
        if self.function is not None:
            self.function()

    def store_action(self, function):
        self.function = function
        
class SaveGameSlot(MenuButton):
    
    def __init__(self, parent, name, text, position, align):
        MenuButton.__init__(self, parent, name, text, position, align)
        self.slot_no = name[-1]
        self.parent = parent
        self.filename = '%s.sv' % name
        self.emtpy_text = text
        
        if os.path.exists('saves/%s' % self.filename):
            self.parent.parent.world.Loader.load(self.filename)
            self.save_name = self.parent.parent.world.Loader.get('slot_name')
            self.text = self.save_name
            self.slot_render()
            self.normal()
            self.load_active = True
        else:
            self.save_name = text
            self.slot_render()
            self.normal()
            self.load_active = False
        
    def slot_render(self, suffix=''):
        self.image = self.render(self.slot_no+'. '+self.save_name+suffix)
        self.rect = self.image.get_rect()
        self.hover()

    def put_char(self, char):
        if len(self.save_name) <= 20:
            self.save_name += char
            self.slot_render('_')
        
    def remove_char(self):
        if len(self.save_name) > 0:
            self.save_name = self.save_name[:-1]
            self.slot_render('_')

    def action(self):
        if self.parent.state == 'save':
            self.parent.set_internal_state('enter_name')
            
            if self.save_name == self.emtpy_text:
                self.save_name = ''
                
            self.slot_render('_')
        else:
            if self.load_active:
                self.post_action()
        
    def post_action(self):
        self.slot_render()
        
        if self.function is not None:
            
            if self.parent.state == 'save':
                self.load_active = True
                self.parent.parent.world.Saver.prepare(self.save_name, \
                    'slot_name')
                    
            self.function(self.filename)
        
class MainMenu(object):
    
    def __init__(self, parent, bg_image_path=None):
        self.parent = parent
        from __init__ import loadImage
        self.__group = pygame.sprite.Group()
        self.loadImage = loadImage
        
        self.world_state = ''
        self.state = 'main'
        
        self.save_function = None
        self.load_function = None
        
        self.sel_button = 0

        if bg_image_path is None:
            self.image = self.loadImage('menu.jpg')
        else:
            self.image = self.loadImage(bg_image_path)
            
        self.rect = self.image.get_rect()

        self.buttons = [MenuButton(self, 'new_game', _("New Game"), 
                (self.rect.width/2, 150), 'center'),
            MenuButton(self, 'save_menu', _("Save Game"), 
                (self.rect.width/2, 250), 'center'),
            MenuButton(self, 'load_menu', _("Load Game"), 
                (self.rect.width/2, 350), 'center'),
            MenuButton(self, 'quit', _("Quit"), \
                (self.rect.width/2, 450), 'center'),]
            
        self.save_slots = [SaveGameSlot(self, 'slot1', _("Empty"), 
                (self.rect.width/4, 150), 'topleft'),
            SaveGameSlot(self, 'slot2', _("Empty"), 
                (self.rect.width/4, 250), 'topleft'),
            SaveGameSlot(self, 'slot3', _("Empty"), 
                (self.rect.width/4, 350), 'topleft'),
            MenuButton(self, 'return', _("Return"), 
                (self.rect.width/4, 450), 'topleft')]
                  
        self.store_action('save_menu', self.show_save_menu)
        self.store_action('load_menu', self.show_load_menu)
        
        for slot in self.save_slots:
            if slot.name == 'return':
                slot.store_action(self.return_to_main)
            else:
                slot.store_action(self.save_or_load)
                
        self.buttons[self.sel_button].hover()
        
        for button in self.buttons:
            self.__group.add(button)
        
    def set_state(self, state):
        self.world_state = state
        
    def set_internal_state(self, state):
        self.state = state
    
    def store_action(self, button_name, function):
        """Stores a function for the menu buttons.
        
        The functions for the following button names have to take parameters:
            
            'save_game' def save_function(filename)
            'laod_game' def load_function(filename)
            
        """
        if button_name == 'save_game':
            self.save_function = function
        elif button_name == 'load_game':
            self.load_function = function
        else:
            for button in self.buttons:
                if button.name == button_name:
                    button.store_action(function)
                
    def show_save_menu(self):
        self.buttons[self.sel_button].normal()
        self.__group.empty()
        
        for button in self.save_slots:
            self.__group.add(button)
            
        self.sel_button = 3
        self.save_slots[self.sel_button].hover()
        self.state = 'save'
        
    def show_load_menu(self):
        self.show_save_menu()
        self.state = 'load'
        
    def save_or_load(self, filename):
        if self.state == 'save':
            self.save_function(filename)
        elif self.state == 'load':
            self.load_function(filename)
           
        self.parent.world.add_delayed_function(self.return_to_main) 
            
    def return_to_main(self):
        if self.state != 'main': 
            self.save_slots[self.sel_button].normal()

        self.__group.empty()
        
        for button in self.buttons:
            self.__group.add(button)
            
        self.sel_button = 0
        self.buttons[self.sel_button].hover()
        
        self.state = 'main'

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
        self.__group.draw(surface)
        
    def resume(self):
        if self.state != 'main':
            self.parent.world.add_delayed_function(self.return_to_main)
            print self.state
            if self.state == 'enter_name':
                slot = self.save_slots[self.sel_button]
                slot.save_name = slot.text
                slot.slot_render()
                 
        self.parent.world.state = 'game'        
    
    def key_loop(self, event):   
        key = event.key         
        if key == K_RETURN: 
            self.key_return()
            
        elif key == K_ESCAPE: 
            
            if self.world_state == 'game': 
                self.resume()
                
        elif self.state == 'enter_name':
                if event.type == KEYDOWN:
                    if key == K_BACKSPACE:
                        self.save_slots[self.sel_button].remove_char()
                    else:
                        self.save_slots[self.sel_button].put_char(event.unicode)
                    
        else:
            
            if key == K_DOWN: 
                self.key_down()
            elif key == K_UP: 
                self.key_up()

    def key_down(self):
        if self.state == 'main': 
            buttons = self.buttons 
        else: 
            buttons = self.save_slots
        
        buttons[self.sel_button].normal()
        
        if not self.sel_button == 3:
            self.sel_button += 1
        else: 
            self.sel_button = 0
            
        buttons[self.sel_button].hover()
    
    def key_up(self):
        if self.state == 'main': 
            buttons = self.buttons 
        else: 
            buttons = self.save_slots
            
        buttons[self.sel_button].normal()
        
        if not self.sel_button == 0: 
            self.sel_button -= 1
        else: 
            self.sel_button = 3
            
        buttons[self.sel_button].hover()
        
    def key_return(self):
        if self.state == 'main': 
            button = self.buttons[self.sel_button]

            if button.name != 'save_menu':
                button.action()
            else:
                if self.world_state == 'game':
                    button.action()
                    
        elif self.state == 'enter_name': 
            self.state = 'save'
            self.save_slots[self.sel_button].post_action()
        else:
            
            self.save_slots[self.sel_button].action()
