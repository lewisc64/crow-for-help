import pygame
import math
import random

GRAVITY = 0.5

entity_types = {}

def entity(ref):
    global entity_types
    entity_types[ref.NAME] = ref
    return ref

def get_entity_types():
    return entity_types.keys()

def create_entity(type_name):
    return entity_types[type_name]()

def rotate_point(x, y, cx, cy, rel_angle):
    rx = x - cx
    ry = y - cy
    
    mag = math.sqrt(rx ** 2 + ry ** 2)
    
    current_angle = math.atan2(ry, rx)
    angle = current_angle + rel_angle

    return cx + mag * math.cos(angle), cy + mag * math.sin(angle)

class Collider:

    def __init__(self, x1, y1, x2, y2, normal_angle):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.normal_angle = normal_angle % (2 * math.pi)
        self.normal_x = math.cos(normal_angle)
        self.normal_y = math.sin(normal_angle)
        self.collide_dist = 10
        self.friction = 0.1
        self.slide = False
        self.wall_tolerance = math.pi / 8
        self.wall_extension = 3

    def __get_y_level(self, x):
        ratio = (x - self.x1) / (self.x2 - self.x1)
        return self.y1 + (self.y2 - self.y1) * ratio

    def __get_x_level(self, y):
        ratio = (y - self.y1) / (self.y2 - self.y1)
        return self.x1 + (self.x2 - self.x1) * ratio

    def within_x_bounds(self, x):
        if self.x1 > self.x2:
            return x >= self.x2 and x <= self.x1
        return x >= self.x1 and x <= self.x2

    def within_y_bounds(self, y):
        if self.y1 > self.y2:
            return y >= self.y2 and y <= self.y1
        return y >= self.y1 and y <= self.y2

    def is_wall(self):
        nx_wall = self.normal_angle >= math.pi - self.wall_tolerance and self.normal_angle <= math.pi + self.wall_tolerance
        px_wall = self.normal_angle >= math.pi * 2 - self.wall_tolerance or self.normal_angle <= self.wall_tolerance
        return nx_wall or px_wall

    def is_ceiling(self):
        return self.normal_angle < math.pi

    def move_rel(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def rotate(self, angle, x=None, y=None):
        if x is None:
            x = (self.x1 + self.x2) / 2
        if y is None:
            y = (self.y1 + self.y2) / 2

        self.x1, self.y1 = rotate_point(self.x1, self.y1, x, y, angle)
        self.x2, self.y2 = rotate_point(self.x2, self.y2, x, y, angle)
        self.normal_x, self.normal_y = rotate_point(self.normal_x, self.normal_y, 0, 0, angle)
        self.normal_angle = (self.normal_angle + angle) % (2 * math.pi)
    
    def collide(self, entity):
        x, y = entity.x, entity.y

        nx_wall = self.normal_angle >= math.pi - self.wall_tolerance and self.normal_angle <= math.pi + self.wall_tolerance
        px_wall = self.normal_angle >= math.pi * 2 - self.wall_tolerance or self.normal_angle <= self.wall_tolerance
        
        if px_wall or nx_wall:
            
            if not self.within_y_bounds(y - self.wall_extension) and not self.within_y_bounds(y + self.wall_extension):
                return False

            collide_dist = max(abs(entity.x_velocity), self.collide_dist)

            collider_x = self.__get_x_level(y)

            if px_wall and x < collider_x + entity.width / 2 and x >= collider_x - collide_dist or nx_wall and x > collider_x - entity.width / 2 and x <= collider_x + collide_dist:
                if px_wall:
                    entity.move_to(collider_x + entity.width / 2, entity.y)
                elif nx_wall:
                    entity.move_to(collider_x - entity.width / 2, entity.y)
                    
                entity.last_collision = self
                entity.x_velocity = 0

        else:
            if not self.within_x_bounds(x):
                return False

            collide_dist = max(abs(entity.y_velocity), self.collide_dist)

            collider_y = self.__get_y_level(x)
                
            if self.is_ceiling():

                if y - entity.height < collider_y and y >= collider_y - collide_dist:
                    entity.y_velocity += self.normal_y
                    entity.x_velocity += self.normal_x
                    entity.move_to(entity.x, collider_y + entity.height)
                    entity.last_collision = self
                    return True

            else:
                
                if y >= collider_y and y <= collider_y + collide_dist:
                    if self.slide:
                        entity.move_rel(self.normal_x, self.normal_y * (y - collider_y))
                    else:
                        entity.move_to(entity.x, collider_y)
                    entity.y_velocity = 0
                    entity.last_collision = self
                    entity.last_floor_collision = self
                    return True
        return False

    def snap_entity_vertically(self, entity):
        x, y = entity.x, entity.y
        if x < self.x1 or x > self.x2:
            return False
        entity.y = self.__get_y_level(x)
        return True

    def debug_draw(self, surface, camera):
        color = (0, 0, 0)
        if self.is_wall():
            color = (128, 255, 0)
        elif self.is_ceiling():
            color = (255, 128, 0)
        pygame.draw.line(surface, color, camera.shift_point((self.x1, self.y1)), camera.shift_point((self.x2, self.y2)))
        
        x = self.x1 + (self.x2 - self.x1) / 2
        y = self.y1 + (self.y2 - self.y1) / 2
        exaggeration = 10
        pygame.draw.line(surface, (255, 0, 0), camera.shift_point((x, y)), camera.shift_point((x + self.normal_x * exaggeration, y + self.normal_y * exaggeration)))

class Entity:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        
        self.width = width
        self.height = height
        
        self.last_collision = None
        self.last_floor_collision = None

        self.collide_with_entities = False
        self.collide_with_terrain = True
        
        self.colliders = []
        self.colliders.append(Collider(x + width, y, x, y, 3 * math.pi / 2))
        self.colliders.append(Collider(x, y, x, y + height, math.pi))
        self.colliders.append(Collider(x + width, y + height, x + width, y, 0))
        self.colliders.append(Collider(x, y + height, x + width, y + height, math.pi / 2))
        for collider in self.colliders:
            collider.move_rel(-self.width / 2, -self.height)
            collider.wall_extension = 0

        self.held_keys = []

    def move_to(self, x, y):
        self.move_rel(x - self.x, y - self.y)

    def move_rel(self, dx, dy):
        self.x += dx
        self.y += dy
        for collider in self.colliders:
            collider.move_rel(dx, dy)

    def rotate(self, angle, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y - self.height / 2
        for collider in self.colliders:
            collider.rotate(angle, x, y)

    def collide(self, entity):
        for collider in self.colliders:
            collider.collide(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.held_keys.append(event.key)
        elif event.type == pygame.KEYUP:
            while event.key in self.held_keys:
                self.held_keys.remove(event.key)

    def update(self, delta, **kwargs):
        self.move_rel(self.x_velocity * delta, self.y_velocity * delta)

    def draw(self, surface, camera, **kwargs):
        pygame.draw.line(surface, (255, 0, 255), camera.shift_point((self.x, self.y)), camera.shift_point((self.x, self.y - self.height)), self.width)
        for collider in self.colliders:
            collider.debug_draw(surface, camera)

@entity
class Player(Entity):

    NAME = "player"

    def __init__(self, x=0, y=0, width=16, height=16):
        super().__init__(x, y, width, height)
        self.upthrust = -GRAVITY * 3
        self.air_acc = 0.3
        self.ground_acc = 0.5

    def dump(self):
        return {
            "name": Player.NAME,
            "x": self.x,
            "y": self.y,
        }

    def load(self, obj):
        self.move_to(obj["x"], obj["y"])

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def update(self, **kwargs):
        super().update(**kwargs)

        self.y_velocity += GRAVITY

        if pygame.K_SPACE in self.held_keys:
            self.y_velocity += self.upthrust
        if pygame.K_a in self.held_keys:
            self.x_velocity -= self.air_acc
        if pygame.K_d in self.held_keys:
            self.x_velocity += self.air_acc

    def handle_event(self, event, **kwargs):
        super().handle_event(event)

    def draw(self, surface, camera, **kwargs):
        super().draw(surface, camera, **kwargs)
