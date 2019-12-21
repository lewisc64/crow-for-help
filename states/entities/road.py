import pygame
from .Entity import *

class Road(Entity):

    def __init__(self, x, y, width=16):
        self.x = x
        self.y = y
