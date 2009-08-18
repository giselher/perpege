from pygame.locals import *
        
class Combat(object):
    
    def __init__(self, parent, display):
        self.parent = parent
        self.display = display
        from __init__ import loadImage, pygame
        self.image = loadImage('interface/Combat_Widget.png')
        self.surface = pygame.Surface((500, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_rect().width/2, 600)
        
        self.font = pygame.font.SysFont('Monospace', 16, True)
        
        self.opponents = {}
        self.player = None 
        

    def draw(self):
        self.surface.blit(self.image, (0, 0))
        self.display.blit(self.surface, self.rect.topleft)