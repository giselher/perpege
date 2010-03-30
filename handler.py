import sys
import parser

class DEQHandler(object):

    def __init__(self, player):
        self.player = player
        self.parser = parser.Parser("content/story/dialogs")
        self.requirements = {}
        self._req_None = None

    def get_dialog(self, dialogs): #too much dialogs :P
        dialog = None
        max = -1

        for dlg in dialogs:

            p_dialog = self.parser.parse_dialog(dlg)
            self.requirements = p_dialog['requirements']

            if self.check_requirements(self.requirements):

                    _len_req = len(self.requirements)

                    if 'events' in self.requirements:
                        _len_req += len(self.requirements['events']) -1

                    if _len_req > max:
                        dialog = p_dialog
                        max = _len_req
            else:
                if max == -1:
                    dialog = p_dialog

        return dialog

    def check_requirements(self, requirements):

        for req in requirements:
            if req == 'events':
                for event in requirements['events']:
                    if not event in self.player.events:
                        return False

            elif req == 'quests':
                for quest in requirements[req]:
                    if self.player.quests[req] != requirements[req][quest]:
                        return False
            else:
                return False

        return True


    def set(self, key, value):
        if key == 'event':
            self.player.events.append(value)

    def _req_events(self, event_list):
        self.requirements['events'] = event_list