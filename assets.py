import pygame
import os
import logging

log = logging.getLogger(__name__)

class AssetManager:

    def __init__(self, folder="assets"):

        self.images = {}

        for path, key in self.discover(folder, "png"):
            log.info(f"loading image '{path}'")
            self.images[key] = pygame.image.load(path).convert_alpha()

    def discover(self, folder, extension):
        out = []
        for item in os.listdir(folder):

            item_path = os.path.join(folder, item)
            
            if "." not in item:
                out.extend(self.discover(item_path, extension))
            elif item.endswith(extension):
                out.append([item_path, ".".join(item_path.replace("\\", ".").split(".")[1:-1])])

        return out
