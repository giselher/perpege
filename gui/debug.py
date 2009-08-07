import pygame

def blit_fps(clock, surface, pos):
    font = pygame.font.SysFont('Monospace', 16, True)
    text = font.render(str(clock.get_fps()), True, (255, 255, 255))
    surface.blit(text, pos)