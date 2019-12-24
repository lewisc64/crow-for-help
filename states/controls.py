import pygame
import time
import logging

from .state import *
from .chase import *
from .pgui import *

log = logging.getLogger(__name__)

class Controls(State):

    def __init__(self, state_stack):
        self.gui = Handler()
        self.gui.add_control(Button("Back", 10, 10, 100, 20, lambda: state_stack.pop()))

    def handle_event(self, event, state_stack, **kwargs):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                state_stack.pop()
                return
        self.gui.handle(event)

    def draw(self, surface, assets, *args, **kwargs):
        surface.blit(assets.images["images.controls"], (0, 0))
        self.gui.draw(surface)
        
