import pygame

from .entity import *

@entity
class Mouse(Entity):

    NAME = "mouse"

    def __init__(self, x=0, y=0, width=16, height=16):
        super().__init__(x, y, width, height)
        # 2.5
        self.speed = 2.5

    def dump(self):
        return {
            "name": Mouse.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def kill(self, state, assets, **kwargs):
        assets.play_sound("sounds.death")
        state.load_by_name(state.level_name)

    def update(self, **kwargs):
        super().update(**kwargs)
        
        self.y_velocity += GRAVITY
        self.x_velocity = self.speed

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.mouse"]
        image = pygame.transform.scale(image, [2 * x for x in image.get_size()])
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))
        if self.lifetime < 200:
            image = assets.images["images.meta.protect_from_harm"]
            surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height() - self.height - 10)))
