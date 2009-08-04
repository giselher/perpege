"""
@author Alexander Preisinger

# DEPTRECATED!

Provides different Containers for the pygame.sprite.Sprite or Group classes.

"""
import pygame.sprite as pg_sprite

# Better off finding a better solution for managing the sprites for drawing.
# Because of the Z-Order of the different sprites and the different layers.
# Something like a handler that places the movable and animated objects 
# independet of other groups between the unmovable objects 


class LayerContainer(object):

    def __init__(self, layers=5):
        """        
        Creates a Container that has layers with a Sprite Group in every layer.
        
        The Layer with the highest rank is 0. The Sprites in this layer will be drawn first 
        than the Sprites from layer 1 and so on.
                
        *************
        Container[layer] --> returns a Group with the sprites in the specified layer
        
        for sprite in Container: --> returns all Sprites ordered by the ranks of the layers
        
        if sprite in Container: --> returns bool
        
        len(Container): --> returns the amount of sprites in the container

        """
        self.__layers = {}
        for layer in range(layers):
            self.__layers[layer] = pg_sprite.Group()

    def insert(self, sprite, layer):
        """Add the sprite into the group/container of the given layer.
        """
        self.__layers[layer].add(sprite)

    def info(self):
        """Returns easy to read information about the class fo debuging.
        """
        string = ''
        for layer in range(len(self.__layers)):
            string += "Layer %d has %s\n" % (layer, self.__layers[layer])
        return string
    
    def draw(self, surface):
        """
        Draws every layer to the given surface.
        """
        for layer in self.__layers:
            self.__layers[layer].draw(surface)
    
    def __iter__(self):
        for layer in range(len(self.__layers)):
            for sprite in self.__layers[layer].sprites():
                yield sprite
        
    def __getitem__(self, key):
        return self.__layers[key]
      
    def __repr__(self):
        return "<%s(%d Layers, %d sprites)>" % (self.__class__.__name__, len(self.__layers), len(self))
    
    def __len__(self):
        count = 0
        for layer in self.__layers:
            count += len(self.__layers[layer])
        return count
    
    def __contains__(self, sprite):
        for itersprite in self:
            if sprite is itersprite:
                return True

class GridMapContainer(object):
    
    def __init__(self, rows=0, cols=0):
        self.__grid = {}
        self.col_count = cols
        self.row_count = rows
        
        for row in range(rows):
            self.__grid[row] = {}
            for col in range(cols):
                self.__grid[row][col] = ''
        
    def getRow(self, row):
        for cell in self.__grid[row]:
            yield cell
        
    def getCell(self, row, col):
        return self.__grid[row][col]
        
    def insert(self, sprite, row, col):
        self.__grid[row][col] = sprite

    def draw(self, surface):
        row_size = self.__grid[0][0].rect.height
        col_size = self.__grid[0][0].rect.width
        for row in self.__grid:
            if y == 0: y = 0
            else: y += row_size       
            for col in self.__grid[row]:
                if x == 0: x = 0
                else: x += col_size 
                surface.blit(self.__grid[row][col], (x, y))
 