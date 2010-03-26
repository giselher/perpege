
class SaAS(object):
    
    def __init__(self):
        
        self.level = 1
        self.exp = 0
        self.next_lvl_exp = 100
        self.spoints = 0
        self.hitpoints = 100
        
        self.attack_type = 'strength'
        
        self.weapon = None
        self.armor = None
        
        #changeable by a level-up
        self.strength = 0
        self.dexterity = 0
        
        #depends on the weapon
        self.damage = 0
        self.precision = 0
        
        #depends on the armor
        self.defence = 0
        self.agility = 0
        
    def level_up(self):
        self.level += 1
        self.spoints += 100 * self.level
        self.hitpoints += hitpoints / 10
        
    def check_exp(self):
        if self.exp >= self.next_lvl_exp:
            self.level_up()
            self.next_lvl_exp += self.next_lvl_exp * self.level
            
    def equip_weapon(self, weapon):
        if weapon.type == 'strengh':
            self.damage = weapon.damage + self.strength
            self.precision = self.dexterity
        else:
            self.damage = weapon.damage
            self.precision = weapon.precision + self.dexterity
            
        self.attack_type = ''
        
        self.weapon = weapon
            
    def remove_weapon(self):
        pass
         
    def equip_armor(self, armor):
        self.defence = armor.defence
        self.agility = int(float(self.dexterity) / 100 * \
            (100 - armor.agility_malus))
        
        self.armor = armor
        
    def remove_armor(self):
        pass
        
    def attack(self, enemy):
        if self.weapon.type == 'strength':
            if self.agility > enemy.agility:
                pass
            elif self.agility == enemy.agility:
                pass
            else:
                pass
                