import pygame
import math
import json
import logging

from .entities import *

log = logging.getLogger(__name__)

class State:

    def __init__(self):
        pass

    def update(self, *args, **kwargs):
        pass

    def handle_event(self, event, *args, **kwargs):
        pass

    def draw(self, surface, *args, **kwargs):
        pass

class Image:

    def __init__(self, x=0, y=0, image_key="", angle=0, scale=1):
        self.x = x
        self.y = y
        self.z = 1
        self.angle = angle
        self.scale = scale
        self.image_key = image_key

    def dump(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "angle": self.angle,
            "scale": self.scale,
            "image_key": self.image_key,
        }

    def get_image(self, assets):
        return assets.images[self.image_key]

    def move_to(self, x, y, z=None):
        self.x = x
        self.y = y
        if z is not None:
            self.z = z

    def load(self, obj):
        self.x = obj["x"]
        self.y = obj["y"]
        self.z = obj["z"]
        self.scale = obj["scale"]
        self.angle = obj["angle"]
        self.image_key = obj["image_key"]

    def draw(self, surface, camera, assets, **kwargs):
        image = self.get_image(assets)
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle * (180 / math.pi))

        width = image.get_width() * self.scale
        height = image.get_height() * self.scale

        if self.scale != 1:
            image = pygame.transform.scale(image, (width, height))

        #if self.z > 1:
        #    image = image.copy()
        #    mask = pygame.Surface(image.get_size())
        #    mask.fill([(1 - (1 / self.z)) * 255 for x in range(3)])
        #    image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
        
        surface.blit(image, camera.shift_point((self.x - width / 2, self.y - height / 2, self.z)))

class Camera:

    class Tracker:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, width, height, target_object=None):
        if target_object is None:
            self.target_object = Camera.Tracker(0, 0)
        else:
            self.target_object = target_object

        self.x = self.target_object.x
        self.y = self.target_object.y
        self.width = width
        self.height = height
        
        self.transition_speed = 15

    def shift_point(self, point):
        x = int(point[0] - self.x + self.width / 2)
        y = int(point[1] - self.y + self.height / 2)
        
        if len(point) == 3:
            z = point[2]
            f = 1 - (1 / z)
            x += (self.width / 2 - x) * f
            #y += (self.height / 2 - y) * f

        return (x, y)

    def shift_point_to_camera(self, point):
        return [int(point[0] + self.x - self.width / 2), int(point[1] + self.y - self.height / 2)]

    def shift_rect(self, rect):
        return [int(rect[0] - self.x + self.width / 2), int(rect[1] - self.y + self.height / 2), rect[2], rect[3]]

    def update(self):
        self.x += (self.target_object.x - self.x) / self.transition_speed
        self.y += (self.target_object.y - self.y) / self.transition_speed

class Base(State):

    def __init__(self, surface, scale=1):
        
        self.scale = scale
        
        self.surface = surface

        self.dimensions = [x * self.scale for x in surface.get_size()]
        
        self.background_layer = pygame.Surface(self.dimensions)
        self.foreground_layer = pygame.Surface(self.dimensions, flags=pygame.SRCALPHA)

        self.camera = Camera(*self.dimensions)
        
        self.entities = []
        self.terrain = []
        self.images_background = []
        self.images_foreground = []

        self.layer_separator = pygame.Surface(self.surface.get_size(), flags=pygame.SRCALPHA)
        self.layer_separator.fill((0, 0, 0, 32))

        self.level_name = None

    def dump(self):
        return {
            "entities": [x.dump() for x in self.entities],
            "terrain": [x.dump() for x in self.terrain],
            "images_background": [x.dump() for x in self.images_background],
            "images_foreground": [x.dump() for x in self.images_foreground],
        }

    def load(self, obj):

        self.entities = []
        self.terrain = []
        self.images_background = []
        self.images_foreground = []
        
        for data in obj["entities"]:
            entity = create_entity(data["name"])
            entity.load(data)
            self.entities.append(entity)

        for data in obj["terrain"]:
            collider = Collider()
            collider.load(data)
            self.terrain.append(collider)            

        for data in obj["images_background"]:
            image = Image()
            image.load(data)
            self.images_background.append(image)

        for data in obj["images_foreground"]:
            image = Image()
            image.load(data)
            self.images_foreground.append(image)

    def load_by_name(self, name):
        try:
            log.info(f"loading 'levels/{name}.json'")
            file = open(f"levels/{name}.json", "r")
            self.load(json.load(file))
            file.close()
            self.level_name = name
        except FileNotFoundError:
            log.error(f"level with name '{name}' not found")

    def save_as(self, name):
        log.info(f"saving 'levels/{name}.json'")
        data = self.dump()
        file = open(f"levels/{name}.json", "w")
        json.dump(data, file)
        file.close()

    def update(self, **kwargs):
        self.camera.update()

    def handle_event(self, event, **kwargs):
        pass

    def draw(self, surface, **kwargs):

        self.background_layer.fill((200, 200, 255))
        self.foreground_layer.fill((0, 0, 0, 0))

        for image in self.images_background:
            image.draw(self.background_layer, self.camera, **kwargs)

        for entity in self.entities:
            entity.draw(self.foreground_layer, self.camera, **kwargs)

        for image in self.images_foreground:
            image.draw(self.foreground_layer, self.camera, **kwargs)

        dest_size = self.surface.get_size()
        surface.blit(pygame.transform.scale(self.background_layer, dest_size), (0, 0))
        #surface.blit(self.layer_separator, (0, 0))
        surface.blit(pygame.transform.scale(self.foreground_layer, dest_size), (0, 0))
