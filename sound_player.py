import os
import pygame
from gtts import gTTS
from utils import app_data_path, resource_path

class SoundPlayer :
    
    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.sound_enabled = config_handler.sound_config["sound_enabled"]
        self.tts_enabled = config_handler.sound_config["tts_enabled"]
        
        # Base Dir — writable folder next to the exe for user-placed SFX files
        self.base_directory = app_data_path(os.path.join("resources", "sfx"))
        
        # Create dir if it does not exist
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            
        # Get paths from the config.
        # If the config path exists, use it directly.
        # If not, fall back to resource_path() to check for a bundled default WAV.
        self.sound_paths = {}
        self.sound_paths["roll_single"] = self._resolve_sound_path(
            self.config_handler.sfx_config["roll_single"], "roll_single.wav"
        )
        self.sound_paths["roll_multiple"] = self._resolve_sound_path(
            self.config_handler.sfx_config["roll_multiple"], "roll_multiple.wav"
        )
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Retrieve sound effects and set volume
        self.sounds = {}
        self.sounds["roll_single"] = self.retrieve_sound("roll_single", 0.1)
        self.sounds["roll_multiple"] = self.retrieve_sound("roll_multiple", 0.1)

    def _resolve_sound_path(self, config_path, bundled_filename):
        """
        Resolve the path for a sound file.
        Priority:
          1. The path stored in the config (user-configured), if the file exists there.
          2. A bundled default WAV included via PyInstaller's --add-data, 
             looked up with resource_path("resources/sfx/<filename>").
          3. Empty string (sound disabled for this slot).
        """
        if config_path and os.path.exists(config_path):
            return config_path
        
        bundled = resource_path(os.path.join("resources", "sfx", bundled_filename))
        if os.path.exists(bundled):
            return bundled
        
        return ""

    def play_sound(self, sound_name):
        if not self.sound_enabled:
            return
        if not self.sounds.get(sound_name):
            return
        self.sounds[sound_name].play()
        
    def retrieve_sound(self, sound_name, volume):
        path = self.sound_paths.get(sound_name, "")
        if not path:
            self.sounds[sound_name] = None
            return None
        
        self.sounds[sound_name] = pygame.mixer.Sound(path)
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
        # Save TTS mp3 next to the exe in a writable location
        tts_path = app_data_path(f"{generated}.mp3")
        tts = gTTS(f"{generated}")
        tts.save(tts_path)
        self.sounds["latest_tts"] = pygame.mixer.Sound(tts_path)
        self.sounds["latest_tts"].set_volume(0.1)
        self.sounds["latest_tts"].play()
        os.remove(tts_path)