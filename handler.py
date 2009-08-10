
class DEQ_Handler(object):
    
    def __init__(self, player):
        self.player = player
        
    def getDialog(self, interlocutor): #too much dialogs :P
        itrl = interlocutor
        _dialogs = interlocutor.dialogs
        available_dialogs=[]
        for dialog in _dialogs:
            if self.checkRequirementsForDialog(_dialogs[dialog]):
                available_dialogs.append(dialog)
                
        if len(available_dialogs) == 1:
            dialog = _dialogs[available_dialogs[0]]
        else:
            dialog = _dialogs[available_dialogs[0]]
            for _dialog in available_dialogs[1:]:
                if len(_dialogs[_dialog]['requirements']) > len(dialog['requirements']):
                    dialog = _dialogs[_dialog]
        
        return dialog
    
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
        key_value = string.split("==")
        key = key_value[0]
        if key.startswith('E_'):
            self.player.events.append(key)
        elif key.startswith('EQ_'):
            self.player.quest_events[key] = key_value[1]
        else:
            print 'set', key
            
                    