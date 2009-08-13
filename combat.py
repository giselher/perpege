import pygame
from pygame.locals import *


class Combat:
    
    def __init__(self, world, display, interface):
        self.world = world
        self.display = display
        self.interface = interface
        self.display_rect = display.get_rect()
        self.image = pygame.Surface((0, 0))
        self.actor_no = {   4 : 75,
                            3 : 112.5,
                            2 : 150,
                            1 : 225
                            }
    
        self.opponents = {}
        self.player = None
        self.font = pygame.font.SysFont('Monospace', 18, True)
        
    def renderText(self, text):
        return self.font.render(text, True, (255, 255, 255))
        
    def initMap(self, surface):
        self.image = surface.copy()
        
    def initFight(self, player, opponents):
        self.player = player
        i = 1
        pos = self.actor_no[len(opponents)]
        for opponent in opponents:
            _pos = pos * i
            self.opponents[opponent.name] = {   'position' : (_pos, self.getLeftY(_pos)),
                                                'image' : opponent.animations['right'][3],
                                                'object' : opponent}
            i += 1
            
        self.world.state = 'combat'
        
    def key_loop(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.world.state = 'game'
            
    def loop(self):
        self.key_loop()
        
    def getLeftY(self, x):
        return (x * -2) + self.display_rect.height 
    
    def getRightY(self, x):
        return (x * 2) - (self.display_rect.height + self.display_rect.height/1.666)
    
    def draw(self):
        self.display.blit(self.image, (0, 0))
        for opnt in self.opponents:
            pos = self.opponents[opnt]['position']
            self.display.blit(self.opponents[opnt]['image'], pos)
            self.display.blit(self.renderText(opnt), (pos[0], pos[1]-30))

        self.display.blit(self.player.animations['left'][3], (799, self.getRightY(799)))
        self.display.blit(self.renderText(self.player.name), (799, self.getRightY(799)-30))