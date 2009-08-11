
class SaAS(object):
    
    def __init__(self):
        
        self.level = 1
        self.exp = 0
        self.hitpoints = 100
        
        #ckangeable by a level-up
        self.strength = 0
        self.dexterity = 0
        
        #depends on the weapon
        self.damage = 0
        self.precision = 0
        
        #depends on the armor
        self.defence = 0
        self.dodge = 0