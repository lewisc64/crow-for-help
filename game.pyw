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

        self.assets = AssetManager("assets")
        self.state_stack = []
        self.state_stack.append(MainMenu(self.assets, self.surface, self.state_stack))

        #entry_level = "win"
        #self.state_stack.append(Chase(self.surface, level_name=entry_level))
        #self.state_stack.append(Editor(self.surface))
        #self.state_stack[-1].load_by_name(entry_level)

    def loop(self):

        clock = pygame.time.Clock()
        dt = 1

        while True:

            if len(self.state_stack) == 0:
                break
            state = self.state_stack[-1]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                state.handle_event(event, state_stack=self.state_stack, assets=self.assets)

            state.update(delta=dt, state_stack=self.state_stack, assets=self.assets)

            state.draw(self.surface, assets=self.assets)

            pygame.display.update()
            ms = clock.tick(FPS)
            dt = ms / (1000 / FPS)        

if __name__ == "__main__":

    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    
    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Crow for Help")

    game = Game(display)
    game.loop()
    pygame.quit()
