import pygame
import time
import logging

from .state import *
from .chase import *
from .pgui import *

log = logging.getLogger(__name__)

class MainMenu(State):

    def __init__(self, assets, surface, state_stack):

        self.init_time = time.time()
        
        self.gui = Handler()
        self.gui.add_control(Button("Play", 10, 10, 100, 20, lambda: self.play(surface, state_stack)))
        self.gui.add_control(Button("Exit", 10, 40, 100, 20, lambda: self.exit(state_stack)))

    def play(self, surface, stack):
        stack.append(Chase(surface, level_name="level_0"))

    def exit(self, stack):
        stack.pop()

    def update(self, assets, **kwargs):
        assets.play_music("menu", volume=0.3)

    def handle_event(self, event, state_stack, **kwargs):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                state_stack.pop()
                return
        self.gui.handle(event)

    def draw(self, surface, assets, *args, **kwargs):
        if time.time() - self.init_time >= 4.25:
            surface.blit(assets.images["images.main_menu"], (0, 0))
            self.gui.draw(surface)
        
