from .base import *
import pygame

class Button(Control):
    
    global_style = {
        "fill":default_global_style["fill"],
        "outline":default_global_style["outline"],
        "text_color":default_global_style["text_color"],
        "depressed_fill":(150, 150, 150),
        "depressed_outline":(200, 200, 200),
        "depressed_text_color":(0, 0, 0),
        "font_name":default_global_style["font_name"],
        "font_size":None,
        "outline_thickness":default_global_style["outline_thickness"],
    }
    
    def __init__(self, text, x, y, width, height, func=None, args=(), kwargs={}):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.func = func
        self.args = args
        self.kwargs = kwargs
        
        self.depressed = False
        
        self.style = Button.global_style.copy()
    
    def update(self):
        super().update()
    
    def handle(self, e):
        
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if self.is_inside(e.pos):
                    self.depressed = True
            return True
            
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                self.depressed = False
                if self.is_inside(e.pos):
                    if self.func is None:
                        return True
                    return self.func(*self.args, **self.kwargs)
        
        return False
    
    def draw(self, surface):
        
        
        font = pygame.font.SysFont(self.style["font_name"], self.style["font_size"] if self.style["font_size"] else self.height)
        rendered = font.render(self.text, 1, self.style["depressed_text_color"] if self.depressed else self.style["text_color"])
        
        if self.depressed:
            fill = self.style["depressed_fill"]
            outline = self.style["depressed_outline"]
        else:
            fill = self.style["fill"]
            outline = self.style["outline"]
        
        pygame.draw.rect(surface, fill, self.get_rect())
        pygame.draw.rect(surface, outline, self.get_rect(), self.style["outline_thickness"])
        surface.blit(rendered, (self.x + self.width // 2 - rendered.get_width() // 2 + (1 if self.depressed else 0), self.y + self.height // 2 - rendered.get_height() // 2))
