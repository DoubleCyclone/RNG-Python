import json
import os
from defaults import *

# Config Handler Class
class ConfigHandler() :    
    
    def __init__(self) :
        self.base_directory = "config/"
        
        # Initialize config paths
        self.preset_config_path = self.base_directory + "preset.json"
        self.style_config_path = self.base_directory + "style.json"
        self.hotkeys_config_path = self.base_directory + "hotkeys.json"
        self.sfx_config_path = self.base_directory + "sfx.json"
        self.sound_config_path = self.base_directory + "sound.json"
        
        # Get default configs
        self.default_preset_config = PRESET
        self.default_hotkeys_config = HOTKEYS
        self.default_style_config = STYLE
        self.default_sfx_config = SFX
        self.default_sound_config = SOUND
        
        # Create base dir if does not exist
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)
        
        # Preset config
        self.preset_config = self.check_saved_config(self.preset_config_path, self.default_preset_config)
        # Style config
        self.style_config = self.check_saved_config(self.style_config_path, self.default_style_config)
        # Hotkey config
        self.hotkeys_config = self.check_saved_config(self.hotkeys_config_path, self.default_hotkeys_config)
        # SFX config
        self.sfx_config = self.check_saved_config(self.sfx_config_path, self.default_sfx_config)
        # Sound config
        self.sound_config = self.check_saved_config(self.sound_config_path, self.default_sound_config)
        
        # Collect all configs
        self.configs = []
        self.configs.append([self.preset_config, self.preset_config_path])
        self.configs.append([self.style_config, self.style_config_path])
        self.configs.append([self.hotkeys_config, self.hotkeys_config_path])
        self.configs.append([self.sfx_config, self.sfx_config_path])
        self.configs.append([self.sound_config, self.sound_config_path])
                
    def check_saved_config(self, config_path, default_config):
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
        else:
            with open(config_path, "w+") as f:
                json.dump(default_config, f, indent=4)
            with open(config_path) as f:
                config = json.load(f)
                
        return config
    
    def save_configs(self):
        for config, path in self.configs :
            with open(path, "w+") as f:
                json.dump(config, f, indent=4)
        
            
        