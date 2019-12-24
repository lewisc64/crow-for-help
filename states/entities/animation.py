import pygame
import time

class Animation:
    
    def __init__(self, sheet, number_of_images, fps, scale=1):
        self.images = []
        self.current_image = 0
        self.slice(sheet, number_of_images, scale=scale)
        self.last_change = time.time()
        self.period = 1 / fps
        self.paused = False
    
    def slice(self, sheet, number_of_images, scale=1):
        x = 0
        image_width = sheet.get_width()
        image_height = sheet.get_height() // number_of_images
        for y in range(0, sheet.get_height(), image_height):
             # "GIVE ME SUBSURFACE" - Central
            self.images.append(pygame.transform.scale(sheet.subsurface((x, y, image_width, image_height)), (image_width * scale, image_height * scale)))
    
    def get_image(self):
        return self.images[self.current_image]
    
    def pause(self):
        self.paused = True
    
    def play(self):
        self.paused = False
    
    def reset(self):
        self.current_image = 0
        
    def restart(self):
        self.reset()
        self.play()
    
    def stop(self):
        self.paused = True
        self.reset()
    
    def update(self):
        if not self.paused:
            this_time = time.time()
            if (this_time - self.last_change) >= self.period:
                self.last_change = this_time
                self.current_image = (self.current_image + 1) % len(self.images)

class Animations:
    
    def __init__(self):
        self.animations = {}
        self.state = ""
    
    def get_animation(self):
        return self.animations[self.state]
    
    def add(self, name, animation):
        self.animations[name] = animation
    
    def get_image(self):
        return self.get_animation().get_image()
    
    def update(self):
        self.get_animation().update()
    
    def set_state(self, state):
        self.state = state
        self.get_animation().restart()
    
    def stop(self):
        self.get_animation().stop()

    def play(self):
        self.get_animation().play()
        
    def reset(self):
        self.get_animation().reset()
        
    def restart(self):
        self.get_animation().restart()
        
    def pause(self):
        self.get_animation().pause()