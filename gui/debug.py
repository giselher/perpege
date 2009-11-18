import pygame

def blit_fps(clock, surface, pos):
    font = pygame.font.SysFont('Monospace', 16, True)
    text = font.render(str(clock.get_fps()), True, (255, 255, 255))
    surface.blit(text, pos)
    
    
def blit_grid(surface, factor, widescreen=False):
    w, h = surface.get_size()
    step_x = w / (4 ** factor)
    step_y = h / (3 ** factor)
    
    line_x = step_x
    line_y = step_y
    
    while line_x <= w:
        pygame.draw.aaline(surface, (255, 255, 255), (line_x, 0), (line_x, h))
        line_x += step_x    
    
    while line_y <= h:
        pygame.draw.aaline(surface, (255, 255, 255), (0, line_y), (w, line_y))
        line_y += step_y
    
    