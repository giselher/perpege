import pygame
from pygame.locals import *


class Combat:
    
    def __init__(self, world, interface):
        self.world = world
        self.display = world.display
        self.interface = interface
        self.display_rect = self.display.get_rect()
        self.image = pygame.Surface((0, 0))
        
        self.outcome = 'unknown'

        self.interface.set_client(self)
    
        self.opponents = {}
        self.player = None
        self.font = pygame.font.SysFont('Monospace', 18, True)
        
    def renderText(self, text):
        return self.font.render(text, True, (255, 255, 255))
        
    def initMap(self, surface):
        self.image = surface.copy()
        
    def Fight(self, player, opponents):
        self.player = player
        self.player.face('right')
        self.outcome = 'unknown'
        
        self.opponent = opponents[0]
        self.opponent.face('left')
        self.interface.start()
            
        self.world.state = 'combat'
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.world.state = self.world.prev_state
            
    def loop(self):
        self.key_loop()

    def draw(self):
        self.display.blit(self.image, (0, 0))
        self.display.blit(self.player.image, (300, 300))
        self.display.blit(self.opponent.image, (600, 300))
        
        self.interface.draw()