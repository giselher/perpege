"""
Perpeg gui elements.
"""
import sys
sys.path.append('../')
from engine.Misc import loadImage

class Interface(object):
    
    def __init__(self, display):
        self.display = display
        
    def showDialog(self):
        pass