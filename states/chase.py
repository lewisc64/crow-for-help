from .state import *
from .entities import *

class Chase(Base):

    def __init__(self, surface, level_name="test"):
        super().__init__(surface)

        self.load_by_name(level_name)

        for entity in self.entities:
            if isinstance(entity, Player):
                self.camera.target_object = entity
                break

    def update(self, **kwargs):
        super().update(**kwargs)
        
        for entity in self.entities:
            entity.update(state=self, **kwargs)

    def handle_event(self, event, **kwargs):
        super().handle_event(event, **kwargs)
        
        for entity in self.entities:
            entity.handle_event(event, state=self, **kwargs)
