import os
import pygame
from gtts import gTTS

class SoundPlayer :
    
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.sound_enabled = config_handler.sound_config["sound_enabled"]
        self.tts_enabled = config_handler.sound_config["tts_enabled"]
        
        # Base Dir
        self.base_directory = "resources/sfx/"
        
        # Create dir if it does not exist
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            
        # Get paths from the config
        self.sound_paths = {}
        self.sound_paths["roll_single"] = self.config_handler.sfx_config["roll_single"] if os.path.exists(self.config_handler.sfx_config["roll_single"]) else ""
        self.sound_paths["roll_multiple"] = self.config_handler.sfx_config["roll_multiple"] if os.path.exists(self.config_handler.sfx_config["roll_multiple"]) else ""
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Retrieve sound effect and set volume
        self.sounds = {}
        self.sounds["roll_single"] = self.retrieve_sound("roll_single", 0.1)
        
        self.sounds["roll_multiple"] = self.retrieve_sound("roll_multiple", 0.1)

    def play_sound(self, sound_name):
        if not self.sound_enabled:
            return
        if not self.sounds[sound_name]:
            return
        self.sounds[sound_name].play()
        
    def retrieve_sound(self, sound_name, volume):
        self.sounds[sound_name] = pygame.mixer.Sound(self.sound_paths[sound_name]) if self.sound_paths[sound_name] is not "" else None
        
        if self.sounds[sound_name] is None:
            return
        
        self.sounds[sound_name].set_volume(volume)
        
        return self.sounds[sound_name]
    
    def enable_disable_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.config_handler.sound_config["sound_enabled"] = self.sound_enabled
        
    def enable_disable_tts(self):
        self.tts_enabled = not self.tts_enabled
        self.config_handler.sound_config["tts_enabled"] = self.tts_enabled    
    
    def play_external_sound(self, generated):
        if not self.tts_enabled:
            return
        tts_path = f"{generated}.mp3"
        tts = gTTS(f"{generated}")
        tts.save(tts_path)
        self.sounds["latest_tts"] = pygame.mixer.Sound(tts_path)
        self.sounds["latest_tts"].set_volume(0.1)
        self.sounds["latest_tts"].play()
        os.remove(tts_path)