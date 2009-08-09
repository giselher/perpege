import textwrap

class Dialog(object):
    
    def __init__(self, parent, display):
        self.parent = parent
        self.display = display
        from __init__ import loadImage, pygame
        self.image = loadImage('interface/Dialog_Widget.png')
        self.surface = pygame.Surface((500, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_rect().width/2, 600)
        
        self.font = pygame.font.SysFont('Monospace', 18)
        
        self.counter = 0
        self.name = None
        self.portrait = None
        self.owner = None
        self.player = None
        self.handler = None
        self.content = None
        self.text = []
        
    def initDialog(self, owner, player, handler):
        _dialogs = owner.dialogs
        available_dialogs = handler.getAvailableDialogs(owner)
        if len(available_dialogs) == 1:
            dialog = owner.dialogs[available_dialogs[0]]
        else:
            dialog = _dialogs[avaible_dialgos[0]]
            for _dialog in avaible_dialogs[1:]:
                if len(_dialogs[_dialog]['requirements']) > len(dialog['requirements']):
                    dialog = _dialog
        
        self.content = dialog['content']
        self.owner = owner
        self.player = player
        self.handler = handler
        self.next()
    
    def render(self, text):
        return self.font.render(text, True, (0, 0, 0))
        
    def next(self):
        _line1 = None
        _str_count = str(self.counter)
        for line in self.content:
            if line.startswith(_str_count):
                _lined = line.split('-')
                _line1 = _lined[1]
                text = self.content[line]

        if _line1 is not None:
            self.counter += 1
            if _line1 == 'player':
                self.name = self.render(self.player.name)
                self.portrait = self.player.portrait
            elif _line1 == 'self':
                self.name = self.render(self.owner.name)
                self.portrait = self.owner.portrait
            
            if _line1 == 'set':
                self.handler.set(text)
            else:
                self.text = []
                text = textwrap.wrap(eval(text), 29)
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
        