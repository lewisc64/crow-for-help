import time
import pygame

from .entity import *
from .player import *

@entity
class CeilingTurret(Entity):

    NAME = "ceiling_turret"

    def __init__(self, x=0, y=0, width=32, height=32):
        super().__init__(x, y, width, height)

        self.firing_period = 0.1
        self.last_shot = time.time()

    def dump(self):
        return {
            "name": CeilingTurret.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def update(self, state, delta, **kwargs):

        for entity in state.entities:
            if isinstance(entity, Player):
                self.collide(entity, delta)
        
        now = time.time()
        if now - self.last_shot >= self.firing_period:
            bullet = Bullet(self.x, self.y)
            bullet.y_velocity = 10
            state.entities.append(bullet)
            self.last_shot = now

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.ceiling_turret"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))
            

@entity
class Bullet(Entity):

    NAME = "bullet"

    def __init__(self, x, y):
        super().__init__(x, y, 1, 1)

        self.collide_with_terrain = False

    def update(self, state, **kwargs):
        super().update(state=state, **kwargs)

        for entity in state.entities[:]:
            if entity == self or isinstance(entity, CeilingTurret):
                continue
            e_x, e_y, e_width, e_height = entity.get_rect()
            if self.x > e_x and self.y > e_y and self.x < e_x + e_width and self.y < e_y + e_height:
                entity.kill(state=state, **kwargs)
                if self in state.entities:
                    state.entities.remove(self)
                return

        if state.camera.shift_point((0, self.y))[1] - 10 > state.camera.height:
            if self in state.entities:
                state.entities.remove(self)

    def draw(self, surface, camera, **kwargs):
        pygame.draw.circle(surface, (255, 255, 0), camera.shift_point((self.x, self.y)), 3)
            
