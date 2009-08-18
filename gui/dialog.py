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
        
        self.selected = 0
        self.choice_dict = {}
        self.choices = []
        self.text = []
        self.boolChoices = False
        
    def key_loop(self, key):
        if key == K_a or key == K_RETURN: 
            if self.boolChoices:
                self.choice = self.selected
                self.next()
            else:
                if not self.next():
                    self.parent.world.state = 'game'
        if self.boolChoices:
            if key == K_UP: 
                if self.selected != 0: self.selected -= 1
            elif key == K_DOWN: 
                if self.selected != (len(self.choices) - 1): self.selected += 1
        
    def initDialog(self, owner, player, handler):
        self.dialog = handler.getDialog(owner.dialogs)
        _content = self.dialog.content.split('\n')
        for line in _content:
            if line.strip() == '':
                _content.remove(line)
        self.content = _content
        self.owner = owner
        self.player = player
        self.handler = handler
        self.next()
        
    def next(self):
        self.text = []
        try:
            if not self.boolChoices:
                _line = self.content.pop(0)
                if _line.startswith('player'):
                    _line = _line.replace('player', 'player_speak')
                elif _line.startswith('self'):
                    _line = _line.replace('self', 'self_speak')
                eval("self.%s" % _line)
                return True
            else:
                self.boolChoices = False
                self.goto(self.choice_dict[self.choices[self.selected]])#
                self.choices = []
                self.choice_dict = {}
                self.selected = 0
        except IndexError:
            return False
        
    def self_speak(self, text):
        for line in textwrap.wrap(text, 29):
            self.text.append(self.render(line))
        self.portrait = self.owner.portrait
        self.name = self.render(self.owner.name)
        
    def player_speak(self, text):
        for line in textwrap.wrap(text, 29):
            self.text.append(self.render(line))
        self.portrait = self.player.portrait
        self.name = self.render(self.player.name)
        
    def add_choice(self, subcontent, summary):
        self.choices.append(summary)
        self.choice_dict[summary] = subcontent
        self.key_loop(K_a)
        
    def show_choice(self):
        self.renderChoice()
        self.boolChoices = True
        
    def goto(self, subcontent):
        _content = eval('self.dialog.%s' % subcontent).split('\n')
        for line in _content:
            if line.strip() == '':
                _content.remove(line)
        self.content = _content
        self.key_loop(K_a)
    
    def set(self, key, value):
        self.handler.set(key, value)
        self.key_loop(K_a)
        
    def fight(self, opp_list):
        if 'self' in opp_list:
            opp_list.remove('self')
            opp_list.append(self.owner)
            
            
        self.parent.world.prev_state = 'itf'
        self.parent.world.combat.initFight(self.player, opp_list)
        self.key_loop(K_a)
        
    def render(self, text):
        return self.font.render(text, True, (0, 0, 0))
    
    def render_selected(self, text):
        return self.font.render(text, True, (255, 255, 255), (0, 0, 0))
    
    def renderChoice(self):
        self.text = []
        for choice in self.choices:
            if self.selected == self.choices.index(choice):
                self.text.append(self.render_selected(choice))
            else:
                self.text.append(self.render(choice))
        
    def draw(self): 
        self.surface.blit(self.image, (0, 0))
        self.surface.blit(self.portrait, (380, 60))
        self.surface.blit(self.name, (382, 32))
        lineno = 31
        for line in self.text:
            self.surface.blit(line, (31, lineno))
            lineno += 18
        if self.boolChoices: self.renderChoice()
        self.display.blit(self.surface, self.rect.topleft)