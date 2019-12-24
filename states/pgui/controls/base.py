class Control:
    
    def __init__(self):
        self.focused = False
    
    def focus(self):
        self.focused = True
    
    def unfocus(self):
        self.focused = False
    
    def get_rect(self):
        return (self.x, self.y, self.width, self.height)
    
    def is_inside(self, pos):
        x, y = pos
        return x >= self.x and x < self.x + self.width and y >= self.y and y < self.y + self.height
    
    def update(self):
        pass
    
    def handle(self, e):
        return False
    
    def draw(self, surface):
        pass

default_global_style = {
    "fill":(200, 200, 200),
    "outline":(150, 150, 150),
    "text_color":(0, 0, 0),
    "font_name":"Calibri",
    "outline_thickness":2
}
