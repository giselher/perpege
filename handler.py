
class DEQ_Handler(object):
    
    def __init__(self, player):
        self.player = player
        
    def getAvailableDialogs(self, interlocutor):
        dialogs = interlocutor.dialogs
        available_dialogs=[]
        for dialog in dialogs:
            if self.checkRequirementsForDialog(dialogs[dialog]):
                available_dialogs.append(dialog)
        
        return available_dialogs
    
    def checkRequirementsForDialog(self, dialog):
        _requirements = dialog['requirements']
        for req in _requirements:
            if req.startswith('E_'):
                if not req in self.player.events: return False
            elif req.startswith('EQ_'):
                if not req in self.player.quest_events: return False
                else: 
                    if self.player.quest_events[req] != _requirements[req]: return False
                    
        return True
                    
    def set(self, string):
        pass
    
        
                    