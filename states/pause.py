import pygame
import logging

from .state import *
from .entities import *
from .pgui import *

log = logging.getLogger(__name__)

class Pause(State):

    def __init__(self, state_stack):
        self.gui = Handler()

        self.gui.add_control(Button("Resume", 10, 10, 100, 20, lambda: state_stack.pop()))
        self.gui.add_control(Button("Quit", 10, 40, 100, 20, lambda: [state_stack.pop(), state_stack.pop()]))

    def handle_event(self, event, state_stack, **kwargs):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                state_stack.pop()
                return
        self.gui.handle(event)

    def draw(self, surface, *args, **kwargs):
        surface.fill((0, 0, 0))
        self.gui.draw(surface)
        
