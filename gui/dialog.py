import textwrap
from pygame.locals import *

class Dialog(object):
    
    def __init__(self, parent, display):
        self.parent = parent
        self.display = display
        from __init__ import loadImage, pygame
        self.image = loadImage('interface/Dialog_Widget.png')
        self.surface = pygame.Surface((500, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_rect().width/2, 600)
        
        self.font = pygame.font.SysFont('Monospace', 16, True)
        
        self.counter = 0
        self.name = None
        self.portrait = None
        self.owner = None
        self.player = None
        self.handler = None
        self.content = None
        self.text = []
        
    def initDialog(self, owner, player, handler):
        self.counter = 0
        self.content = handler.getDialog(owner)['content']
        self.owner = owner
        self.player = player
        self.handler = handler
        self.next()
    
    def key_loop(self, key):
        if key == K_a: 
            if not self.next():
                self.parent.world.itf = False
    
    def render(self, text):
        return self.font.render(text, True, (0, 0, 0))
        
    def next(self):
        _line1 = None
        _str_count = str(self.counter)
        for line in self.content:
            if line.startswith(_str_count):
                _line1 = line.split('-')[1]
                text = self.content[line]
                if _line1 == 'set': 
                    self.handler.set(text)
                    _line1 = None
                    self.counter += 1

        if _line1 is not None:
            self.counter += 1
            if _line1 == 'player':
                self.name = self.render(self.player.name)
                self.portrait = self.player.portrait
            elif _line1 == 'self':
                self.name = self.render(self.owner.name)
                self.portrait = self.owner.portrait
            

            self.text = []
            text = textwrap.wrap(eval(text), 32)
            for line in text:
                self.text.append(self.render(line))
            return True
        else:
            return False
        
        
    def draw(self): 
        self.surface.blit(self.image, (0, 0))
        self.surface.blit(self.portrait, (380, 60))
        self.surface.blit(self.name, (382, 32))
        lineno = 31
        for line in self.text:
            self.surface.blit(line, (31, lineno))
            lineno += 18
        self.display.blit(self.surface, self.rect.topleft)
        