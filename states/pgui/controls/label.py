from .base import *
import pygame

class Label(Control):

    global_style = {
        "text_color":default_global_style["text_color"],
        "font_name":default_global_style["font_name"],
        "font_size":None,
    }
    
    def __init__(self, text, x, y, font_size=16):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        
        self.style = Label.global_style.copy()
        self.style["font_size"] = font_size
    
    def draw(self, surface):
        
        
        font = pygame.font.SysFont(self.style["font_name"], self.style["font_size"])
        rendered = font.render(self.text, 1, self.style["text_color"])
        
        surface.blit(rendered, (self.x, self.y))
