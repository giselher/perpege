import textwrap
import pygame
from pygame.locals import *

class Dialog(object):

    def __init__(self, parent, display):
        self.parent = parent
        self.display = display
        self.key_map = self.parent.world.key_map

        self.image = self.parent.load_image('interface/Dialog_Widget.png')
        self.surface = pygame.Surface((500, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_rect().width/2, 600)

        self.font = pygame.font.SysFont('Monospace', 16, True)

  #      self.fight_eventualities = {'win':'', 'lose':''}
  #      self.fight_outcome = 'unknown'

        self.lines_per_window = 8 # lines per window

        # Shows the contents after various choices but not after gotos.
        # And it works only for the content not subcontents
        self.post_content = []

        self.selected = 0
        self.choices_dict = {}
        self.choices_list = []
        self.text = []
        self.bool_choices = False

    def key_loop(self, event):
        key = event.key

        if key == self.key_map['action'] or key == K_RETURN:
            self.next()

        if self.bool_choices:
            if key == self.key_map['up']:
                if self.selected != 0: self.selected -= 1

            elif key == self.key_map['down']:
                if self.selected != (len(self.choices_list) - 1):
                    self.selected += 1

    def init_dialog(self, owner, player, handler):
        dialog = handler.get_dialog(owner.dialogs)
        self.owner = owner
        self.player = player
        self.handler = handler
        self.dialog = dialog
        self.content = dialog['content']
        self.next()

    def next(self):
        self.text = []

        if self.bool_choices:
                self.bool_choices = False
                self.goto( \
                    [self.choices_dict[self.choices_list[self.selected]]])
                self.choices_list = []
                self.choices_dict = {}
                self.selected = 0

    #        elif self.fight_outcome != 'unknown':
    #            outcome = self.fight_outcome
    #            self.fight_outcome = 'unknown'
    #            self.goto(self.fight_eventualities[outcome])
        else:

            if len(self.content):
                statement = self.content.pop(0)
                eval("self.%s(%s)" % (statement[0], str(statement[1:])))

            else:
                if len(self.post_content):
                    self.content = self.post_content
                    self.skip()
                else:
                    self.finish()

    def render_text(self, text, talker):
        lines = textwrap.wrap(text, 29)

        if len(lines) > self.lines_per_window:
            render_lines = lines[0:self.lines_per_window-1]
            self.content.insert(0, ("say", talker, \
                " ".join(lines[self.lines_per_window:])))
        else:
            render_lines = lines

        for line in render_lines:
            self.text.append(self.render(line))

    def say(self, args):
        if args[0] == "self":
            talker = self.owner
        elif args[0] == "player":
            talker = self.player
        self.portrait = talker.portrait
        self.name = self.render(talker.name)
        self.render_text(args[1], args[0])

    def choices(self, args):
        for choice in args[0]:
            self.choices_list.append(choice[1])
            self.choices_dict[choice[1]] = choice[0]

        self.content.reverse()
        for statement in self.content:
            self.post_content.insert(0, statement)

        self.render_choices()
        self.bool_choices = True

    def goto(self, args):
        self.content = self.dialog[args[0]][:]
        self.skip()

    def set(self, args):
        self.handler.set(args[0], args[1])
        self.skip()

 #   def fight(self, opp_list):
 #       if 'self' in opp_list:
 #           opp_list.remove('self')
 #           opp_list.append(self.owner)

 #       self.parent.world.prev_state = 'itf'
 #       self.parent.world.combat.Fight(self.player, opp_list)

 #   def set_fight_outcome(self, key, subcontent):
 #       self.fight_eventualities[key] = subcontent
 #       self.skip()

    def skip(self):
        self.next()

    def render(self, text):
        return self.font.render(text, True, (0, 0, 0))

    def render_selected(self, text):
        return self.font.render(text, True, (255, 255, 255), (0, 0, 0))

    def render_choices(self):
        self.text = []
        for choice in self.choices_list:
            if self.selected == self.choices_list.index(choice):
                self.text.append(self.render_selected(choice))
            else:
                self.text.append(self.render(choice))

    def draw(self):
        self.surface.blit(self.image, (0, 0))
        self.surface.blit(self.portrait, (380, 60))
        self.surface.blit(self.name, (382, 32))

        lineno = 31
        for line in self.text:
            self.surface.blit(line, (31, lineno))
            lineno += 18

        if self.bool_choices:
            self.render_choices()

        self.display.blit(self.surface, self.rect.topleft)

    def finish(self):
        self.content = []
        self.text =  []
        self.post_content = []
        self.parent.world.state = 'game'