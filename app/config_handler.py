import json
import os

# Config Handler Class
class ConfigHandler() :    
    
    def __init__(self) :
        self.base_directory = "config/"
        
        self.style_config_path = self.base_directory + "style.json"
        self.hotkeys_config_path = self.base_directory + "hotkeys.json"
        self.sfx_config_path = self.base_directory + "sfx.json"
        
        self.default_hotkeys_config = {"roll_single" : "<ctrl>+<alt>+1", "roll_multiple" : "<ctrl>+<alt>+2"}
        self.default_style_config = {}
        self.default_sfx_config = {"roll_single" : "resources/sfx/dice_roll.wav", "roll_multiple" : "resources/sfx/dice_roll.wav"}
        
        # Create base dir if does not exist
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)
        
        # Layout config
        if os.path.exists(self.style_config_path):
            with open(self.style_config_path) as f:
                self.style_config = json.load(f)
        else:
            with open(self.style_config_path, "w+") as f:
                json.dump(self.default_style_config, f, indent=4)
            with open(self.style_config_path) as f:
                self.style_config = json.load(f)
        
        # Hotkey config
        if os.path.exists(self.hotkeys_config_path):
            with open(self.hotkeys_config_path) as f:
                self.hotkeys_config = json.load(f)
        else:
            with open(self.hotkeys_config_path, "w+") as f:
                json.dump(self.default_hotkeys_config, f, indent=4)
            with open(self.hotkeys_config_path) as f:
                self.hotkeys_config = json.load(f)
                
        # SFX Config
        if os.path.exists(self.sfx_config_path):
            with open(self.sfx_config_path) as f:
                self.sfx_config = json.load(f)
        else:
            with open(self.sfx_config_path, "w+") as f:
                json.dump(self.default_sfx_config, f, indent=4)
            with open(self.sfx_config_path) as f:
                self.sfx_config = json.load(f)
        
            
        