import logging

from .entity import *
from .player import *
from .mouse import *

log = logging.getLogger(__name__)

@entity
class PushBlock(Entity):

    NAME = "push_block"
    
    def __init__(self, x=0, y=0, width=32, height=32):
        super().__init__(x, y, width, height)

    def dump(self):
        return {
            "name": PushBlock.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def update(self, state, **kwargs):
        super().update(state=state, **kwargs)

        self.y_velocity += GRAVITY
        
        player = None
        mouse = None
        for entity in state.entities:
            if entity == self:
                continue
            if isinstance(entity, Player):
                player = entity
            elif isinstance(entity, Mouse):
                mouse = entity

        self.colliders[0].collide(player, kwargs["delta"])
        player.collide(self, kwargs["delta"])
        self.collide(mouse, kwargs["delta"])

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.push_block"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))

@entity
class PushBlockSpikes(PushBlock):

    NAME = "push_block_spikes"

    def dump(self):
        return {
            "name": PushBlockSpikes.NAME,
            "x": self.x,
            "y": self.y,
        }

    def update(self, state, **kwargs):
        super().update(state=state, **kwargs)
        for entity in state.entities:
            if entity == self:
                continue
            if collide_rect((self.x - self.width / 2, self.y - self.height * 1.5, self.width, self.height / 2), entity.get_rect()):
                entity.kill(state=state, **kwargs)
            if isinstance(entity, PushBlock):
                self.collide(entity, kwargs["delta"])

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.push_block_spikes"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))

@entity
class PushBlockSpikesUp(PushBlock):

    NAME = "push_block_spikes_up"

    def __init__(self, x=0, y=0, width=96, height=32):
        super().__init__(x, y, width, height)
        for x in range(3):
            self.colliders.pop(0)

    def dump(self):
        return {
            "name": PushBlockSpikesUp.NAME,
            "x": self.x,
            "y": self.y,
        }

    def update(self, state, **kwargs):
        for entity in state.entities:
            if entity == self:
                continue
            if collide_rect((self.x - self.width / 2, self.y - self.height * 1.5, self.width, self.height / 2), entity.get_rect()):
                entity.kill(state=state, **kwargs)

            bottom_rect = (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height / 2)

            if collide_rect(bottom_rect, entity.get_rect()):
                self.y = entity.y - entity.height

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.push_block_spikes_up"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))


@entity
class SpikeDoor(Entity):

    NAME = "spike_door"
    
    def __init__(self, x=0, y=0, width=32, height=32):
        super().__init__(x, y, width, height)
        self.colliders.pop()
        self.colliders.pop(0)
        self.colliders.pop(0)
        self.colliders[0].wall_extension = 10
        self.collide_with_terrain = False
        self.collide_with_entities = False

    def dump(self):
        return {
            "name": SpikeDoor.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def update(self, state, assets, **kwargs):
        player = None
        for entity in state.entities:
            if entity == self:
                continue
            
            if isinstance(entity, Player):
                player = entity
            
            if collide_rect((self.x - self.width / 2, self.y - self.height, self.width / 2, self.height), entity.get_rect()):
                entity.kill(state=state, assets=assets, **kwargs)

        if self.collide(player, kwargs["delta"]):
            assets.play_sound("sounds.open")
            self.move_rel(0, -self.height)
            self.colliders.pop()

    def draw(self, surface, camera, assets, **kwargs):
        image = assets.images["images.entities.spike_door"]
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))
