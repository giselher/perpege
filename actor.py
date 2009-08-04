from Object import AnimatedObject

class SAS:
    pass

class Actor(AnimatedObject, SAS):

    def __init__(self, animations, position, col_rect, sas_id=None):
        AnimatedObject.__init__(self, animations, position, col_rect)
        self.id = sas_id
        
        
class Player(Actor):
    
    def __init__(self):
        Actor.__init__(self)
