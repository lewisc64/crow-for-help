import pygame
import time
import random

from .entity import *
from .animation import *

@entity
class Player(Entity):

    NAME = "player"

    def __init__(self, x=0, y=0, width=16, height=16):
        super().__init__(x, y, width, height)
        self.upthrust = -GRAVITY * 3
        self.air_acc = 0.5
        self.ground_acc = 0.5
        self.max_vertical_air_speed = 10
        self.max_horizontal_air_speed = 10
        self.max_ground_speed = 3
        self.was_flying = False

        self.last_step_time = time.time()

        self.animations = None
        self.moving_left = False

    def dump(self):
        return {
            "name": Player.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def is_flying(self):
        return self.air_time > 1

    def kill(self, state, assets, **kwargs):
        assets.play_sound("sounds.death")
        state.load_by_name(state.level_name)

    def setup_animations(self, assets):
        self.animations = Animations()
        self.animations.add("fly", Animation(assets.images["images.animations.player_flying"], 8, 30, scale=2))
        self.animations.add("run", Animation(assets.images["images.animations.player_running"], 4, 0.001, scale=2)) # 15
        self.animations.set_state("fly")

    def update(self, state, assets, **kwargs):
        super().update(**kwargs)

        if self.animations is None:
            self.setup_animations(assets)
        else:
            self.animations.update()

        self.y_velocity += GRAVITY

        if pygame.K_SPACE in self.held_keys:
            if self.animations.state != "fly":
                self.animations.set_state("fly")
            if not self.is_flying():
                self.y_velocity = 0
                self.move_rel(0, -1)
            self.y_velocity += self.upthrust

        move_horz = False
        
        if pygame.K_a in self.held_keys:
            self.x_velocity -= self.air_acc
            move_horz = True
        if pygame.K_d in self.held_keys:
            self.x_velocity += self.air_acc
            move_horz = True

        if not self.is_flying():

            if not move_horz:
                self.x_velocity *= 0.8
            
            if self.x_velocity > self.max_ground_speed:
                self.x_velocity = self.max_ground_speed
            if self.x_velocity < -self.max_ground_speed:
                self.x_velocity = -self.max_ground_speed

        else:
            self.x_velocity = max(-self.max_horizontal_air_speed, min(self.max_horizontal_air_speed, self.x_velocity))
            self.y_velocity = max(-self.max_vertical_air_speed, self.y_velocity)
            if pygame.K_s not in self.held_keys:
                self.y_velocity = min(self.max_vertical_air_speed, self.y_velocity)

        if self.x_velocity < 0:
            self.moving_left = True
        else:
            self.moving_left = False

        if self.was_flying and not self.is_flying():
            self.animations.set_state("run")
            assets.play_sound("sounds.step_1")
            
        elif not self.was_flying and not self.is_flying():
            f = abs(self.x_velocity) / self.max_ground_speed
            if f != 0:
                self.animations.animations["run"].period = 1 / (15 * f)
                now = time.time()
                if self.x_velocity != 0 and now - self.last_step_time >= 0.2 / f:
                    self.last_step_time = now
                    assets.play_sound(f"sounds.step_{random.randint(1, 3)}")
            
        self.was_flying = self.is_flying()

        self.air_time += 1

        self.x = max(-state.camera.width / 2, self.x)

    def handle_event(self, event, **kwargs):
        super().handle_event(event)

    def draw(self, surface, camera, **kwargs):
        if self.animations is None:
            pygame.draw.line(surface, (0, 0, 0), camera.shift_point((self.x, self.y)), camera.shift_point((self.x, self.y - self.height)), self.width)
        else:
            image = self.animations.get_image()
            if self.moving_left:
                image = pygame.transform.flip(image, True, False)
            surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height())))
