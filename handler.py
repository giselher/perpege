import sys

class DEQ_Handler(object):
    
    def __init__(self, player):
        self.player = player
        
    def getDialog(self, dialogs): #too much dialogs :P
        sys.path.append('content/story/dialogs')
        dialog = None
        max = -1
        for dlg in dialogs:
            module = __import__(dlg) 
            if module.requirements is not None:
                if self.checkRequirementsForDialog(module.requirements):
                    _len_req = module.requirements
                    if len(_len_req) > max:
                        dialog = module
                        max = _len_req
            else:
                if max == -1:
                    dialog = module

        return dialog
    
    def checkRequirementsForDialog(self, requirements):
        for req in requirements:
            if req == 'events':
                for event in requirements['events']:
                    if not event in self.player.events:
                        return False
                    
            elif req in self.player.quest_events:
                if self.player.quest_events[req] != requirements[req]:
                    return False
            else:
                return False
            
        return True
            

    def set(self, key, value):
        if key == 'event':
            self.player.events.append(value)
                    