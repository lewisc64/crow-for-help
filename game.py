import pygame
import logging

from states import *
from assets import *

FPS = 60

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class Game:

    def __init__(self, surface):
        self.surface = surface
        self.state_stack = []

        self.state_stack.append(Chase(self.surface))
        self.state_stack.append(Editor(self.surface))

        self.assets = AssetManager("assets")

    def loop(self):

        clock = pygame.time.Clock()
        dt = 1

        while True:

            state = self.state_stack[-1]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                state.handle_event(event, assets=self.assets)

            state.update(delta=dt, state_stack=self.state_stack, assets=self.assets)

            state.draw(self.surface, assets=self.assets)

            pygame.display.update()
            ms = clock.tick(FPS)
            dt = ms / (1000 / FPS)        

if __name__ == "__main__":

    pygame.init()

    display = pygame.display.set_mode((800, 600))

    game = Game(display)
    log.debug(game.assets.images)
    game.loop()
