import pygame
from pygame.locals import *
        
class Combat(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.display = parent.display
        from __init__ import loadImage
        self.image = loadImage('interface/timeline.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.display.get_rect().width/2, 550)
        self.font = pygame.font.SysFont('Monospace', 16, True)
        
        self.face_friend_frame = loadImage('interface/face_frame.png')
        self.face_foe_frame = pygame.transform.flip(self.face_friend_frame, False, True)
        pygame.draw.rect(self.face_friend_frame, (145, 255, 145), \
            pygame.Rect(2, 2, 50, 50))        
        pygame.draw.rect(self.face_foe_frame, (250, 75, 65), \
            pygame.Rect(2, 18, 50, 50))
        #pygame.draw.rect(
                
        self.client = None
        
        self.faces = {} 
        self.opponents = []
        self.player = None 
        
    def set_client(self, client):
        self.client = client
        
    def start(self):        
        self.player_face = self.face_friend_frame.copy()
        self.player_face.blit(pygame.transform.scale( \
            self.client.player.portrait, (50, 50)), (2, 2))     
        self.opponent_face = self.face_foe_frame.copy()
        self.opponent_face.blit(pygame.transform.scale( \
            self.client.opponent.portrait, (50, 50)), (2, 18))
    
    def draw(self):
        self.image.blit(self.player_face, (27, 30))
        self.image.blit(self.opponent_face, (27, 100))
        self.display.blit(self.image, self.rect.topleft)