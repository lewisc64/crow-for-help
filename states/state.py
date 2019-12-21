import pygame
import math
import json
import logging

from .entities import *

log = logging.getLogger(__name__)

class State:

    def __init__(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass

class Image:

    def __init__(self, x=0, y=0, image_key="", angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.image_key = image_key

    def dump(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "image_key": self.image_key,
        }

    def get_image(self, assets):
        return assets.images[self.image_key]

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def load(self, obj):
        self.x = obj["x"]
        self.y = obj["y"]
        self.angle = obj["angle"]
        self.image_key = obj["image_key"]

    def draw(self, surface, camera, assets, **kwargs):
        image = pygame.transform.rotate(self.get_image(assets), self.angle * (180 / math.pi))
        surface.blit(image, camera.shift_point((self.x - image.get_width() / 2, self.y - image.get_height() / 2)))

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
        return [int(point[0] - self.x + self.width / 2), int(point[1] - self.y + self.height / 2)]

    def shift_point_to_camera(self, point):
        return [int(point[0] + self.x - self.width / 2), int(point[1] + self.y - self.height / 2)]

    def shift_rect(self, rect):
        return [int(rect[0] - self.x + self.width / 2), int(rect[1] - self.y + self.height / 2), rect[2], rect[3]]

    def update(self):
        self.x += (self.target_object.x - self.x) / self.transition_speed
        self.y += (self.target_object.y - self.y) / self.transition_speed

class Base(State):

    def __init__(self, surface):
        self.surface = surface

        self.camera = Camera(*surface.get_size())
        
        self.entities = []
        self.terrain = []
        self.images_background = []
        self.images_foreground = []

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
            pass

        for data in obj["images_background"]:
            image = Image()
            image.load(data)
            self.images_background.append(image)

        for data in obj["images_foreground"]:
            image = Image()
            image.load(data)
            self.images_foreground.append(image)

    def load_by_name(self, name):
        log.info(f"loading 'levels/{name}.json'")
        file = open(f"levels/{name}.json", "r")
        self.load(json.load(file))
        file.close()

    def save_as(self, name):
        log.info(f"saving 'levels/{name}.json'")
        file = open(f"levels/{name}.json", "w")
        json.dump(self.dump(), file)
        file.close()

    def update(self, **kwargs):
        self.camera.update()

    def handle_event(self, event, **kwargs):
        pass

    def draw(self, surface, **kwargs):

        surface.fill((180, 200, 255))

        for image in self.images_background:
            image.draw(self.surface, self.camera, **kwargs)
        
        for entity in self.entities:
            entity.draw(self.surface, self.camera, **kwargs)

        for image in self.images_foreground:
            image.draw(self.surface, self.camera, **kwargs)
