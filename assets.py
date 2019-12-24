import pygame
import os
import logging

log = logging.getLogger(__name__)

class AssetManager:

    def __init__(self, folder="assets"):

        self.images = {}
        self.audio = {}

        for path, key in self.__discover(folder, "png"):
            log.info(f"loading image '{path}'")
            self.images[key] = pygame.image.load(path).convert_alpha()

        for path, key in self.__discover(folder, "wav"):
            log.info(f"loading audio '{path}'")
            self.audio[key] = pygame.mixer.Sound(path)
        
        self.max_sound_channels = 8
        self.current_music = ""
        self.mute = False

    def __discover(self, folder, extension):
        out = []
        for item in os.listdir(folder):

            item_path = os.path.join(folder, item)
            
            if "." not in item:
                out.extend(self.__discover(item_path, extension))
            elif item.endswith(extension):
                out.append([item_path, ".".join(item_path.replace("\\", ".").split(".")[1:-1])])

        return out
        
    def play_sound(self, name, loop=False, volume=1):
        if self.mute:
            return
        for n in range(self.max_sound_channels):
            if not pygame.mixer.Channel(n).get_busy():
                pygame.mixer.Channel(n).set_volume(volume)
                if loop:
                    pygame.mixer.Channel(n).play(self.audio[name], loops=-1)
                else:
                    pygame.mixer.Channel(n).play(self.audio[name])
                break

    def stop_sound(self, name):
        if self.mute:
            return
        self.sounds[name].stop()
    
    def purge_sounds(self):
        if self.mute:
            return
        for n in range(self.max_sound_channels):
            if pygame.mixer.Channel(n).get_busy():
                pygame.mixer.Channel(n).stop()
    
    def play_music(self, name="", volume=1):
        if not self.mute and name != self.current_music:
            path = "assets/music/{}.ogg".format(name)
            self.current_music = name
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(volume)
            
    
    def resume_music(self):
        if self.mute:
            return
        pygame.mixer.music.unpause()
    
    def pause_music(self):
        if self.mute:
            return
        pygame.mixer.music.pause()
