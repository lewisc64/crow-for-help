import pygame

class Handler:
    
    def __init__(self):
        
        self.background = None
        self.controls = []
    
    def add_control(self, control):
        self.controls.append(control)
    
    def handle(self, e):
        for i, control in enumerate(self.controls):
            if control.handle(e):
                self.controls[0], self.controls[i] = self.controls[i], self.controls[0]
                control.focus()
                for x in self.controls[1:]:
                    x.unfocus()
    
    def draw(self, surface):
        for control in self.controls:
            control.draw(surface)
