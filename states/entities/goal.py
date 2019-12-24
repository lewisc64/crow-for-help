from .entity import *
from .mouse import *

@entity
class Goal(Entity):

    NAME = "goal"

    def __init__(self, x=0, y=0, width=16, height=16):
        super().__init__(x, y, width, height)

    def dump(self):
        return {
            "name": Goal.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def update(self, state, **kwargs):
        for entity in state.entities:
            if isinstance(entity, Mouse):
                if collide_rect(entity.get_rect(), self.get_rect()):
                    state.win()

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.goal"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))
