import os
import pygame

class SoundPlayer :
    
    def __init__(self, config_handler):
        # Base Dir
        self.base_directory = "resources/sfx/"
        
        # Create dir if it does not exist
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            
        # Get paths from the config
        self.sound_paths = {}
        self.sound_paths["roll_single"] = config_handler.sfx_config["roll_single"] if os.path.exists(config_handler.sfx_config["roll_single"]) else ""
        self.sound_paths["roll_multiple"] = config_handler.sfx_config["roll_multiple"] if os.path.exists(config_handler.sfx_config["roll_multiple"]) else ""
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Retrieve sound effect and set volume
        self.sounds = {}
        self.sounds["roll_single"] = self.retrieve_sound("roll_single", 0.1)
        
        self.sounds["roll_multiple"] = self.retrieve_sound("roll_multiple", 0.1)

    def play_sound(self, sound_name):
        if not self.sounds[sound_name]:
            return
        self.sounds[sound_name].play()
        
    def retrieve_sound(self, sound_name, volume):
        self.sounds[sound_name] = pygame.mixer.Sound(self.sound_paths[sound_name]) if self.sound_paths[sound_name] is not "" else None
        
        if self.sounds[sound_name] is None:
            return
        
        self.sounds[sound_name].set_volume(volume)
        
        return self.sounds[sound_name]