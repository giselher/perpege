import pygame
from pygame.locals import *

class Combat(object):

    def __init__(self, world):
        self.world = world
        self.display = world.display
        self.interface = GUI(self)
        self.display_rect = self.display.get_rect()
        self.image = pygame.Surface((0, 0))

        self.outcome = 'unknown'

        self.interface.set_client(self)

        self.opponents = {}
        self.player = None
        self.font = pygame.font.SysFont('Monospace', 18, True)

    def renderText(self, text):
        return self.font.render(text, True, (255, 255, 255))

    def init_map(self, surface):
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

class GUI(object):

    def __init__(self, parent):
        self.parent = parent
        self.display = parent.display
        self.load_image = parent.world.load_image
        self.image = self.load_image('interface/timeline.png')

        self.actors = []

        self.rect = self.image.get_rect()
        self.rect.midtop = (self.display.get_rect().width/2, 550)
        self.font = pygame.font.SysFont('Monospace', 16, True)

        self.face_friend_frame = self.load_image('interface/face_frame.png')
        self.face_foe_frame = \
            pygame.transform.flip(self.face_friend_frame, False, True)

        pygame.draw.rect(self.face_friend_frame, (145, 255, 145), \
            pygame.Rect(2, 2, 50, 50))
        pygame.draw.rect(self.face_foe_frame, (250, 75, 65), \
            pygame.Rect(2, 18, 50, 50))

        self.client = None

        self.faces = {}
        self.opponents = []
        self.player = None

    def init_gui(self):
        pass

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

    def move(self):
        pass

class Face(object):

    def __init__(self):
        pass