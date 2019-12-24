import logging

from .state import *
from .pause import *
from .entities import *

log = logging.getLogger(__name__)

class Chase(Base):

    def __init__(self, surface, level_name="test"):
        super().__init__(surface)

        self.load_by_name(level_name)

    def win(self):
        log.info("win, load next level")
        self.load_by_name(f"level_{int(self.level_name.split('_')[1])+1}")

    def load_by_name(self, name):
        super().load_by_name(name)
        for entity in self.entities:
            if isinstance(entity, Player):
                self.camera.target_object = entity
                break

    def update(self, **kwargs):
        super().update(**kwargs)

        kwargs["assets"].play_music("level", volume=0.3)
        
        for entity in self.entities:
            entity.update(state=self, **kwargs)

            if entity.collide_with_terrain:
                for collider in self.terrain:
                    collider.collide(entity, kwargs["delta"])

    def handle_event(self, event, state_stack, **kwargs):
        super().handle_event(event, **kwargs)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                state_stack.append(Pause(state_stack))
        
        for entity in self.entities:
            entity.handle_event(event, state=self, **kwargs)

    def draw(self, *args, **kwargs):
        self.camera.x = max(0, self.camera.x)
        self.camera.y = 0
        super().draw(*args, **kwargs)
