import pygame
from pygame.locals import *

class Dialog(pygame.sprite.Sprite):
    
    def __init__(self, display):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.image = pygame.Surface((500, 200))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_rect().width/2, 600)
        
    def draw(self): 
        self.display.blit(self.image, self.rect.topleft)