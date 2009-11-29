import sys
import reader

class DEQ_Handler(object):
    
    def __init__(self, player):
        self.player = player
        self.dlg_reader = reader.Reader("content/story/dialogs")
        self.requirements = {}
        self._req_None = None
        
    def getDialog(self, dialogs): #too much dialogs :P
        dialog = None
        max = -1
        for dlg in dialogs:
            self.requirements.clear()
            parsed_dialog = self.dlg_reader.readDlgFile(dlg)
            requirements = parsed_dialog['requirements']
            
            for req in requirements:
                exec("self._req_%s" % req)

            if self.checkRequirementsForDialog(self.requirements):
                    _len_req = len(self.requirements)
                    if 'events' in self.requirements: 
                        _len_req += len(self.requirements['events']) -1
                    if _len_req > max:
                        dialog = parsed_dialog
                        max = _len_req
            else:
                if max == -1:
                    dialog = parsed_dialog

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
        
    def _req_events(self, event_list):
        self.requirements['events'] = event_list