import json
import os

# Config Handler Class
class ConfigHandler() :    
    
    def __init__(self) :
        self.style_config_path = "config/style.json"
        self.hotkeys_config_path = "config/hotkeys.json"
        
        self.default_hotkeys_config = {"roll_single" : "<ctrl>+<alt>+1", "roll_multiple" : "<ctrl>+<alt>+2"}
        self.default_style_config = {}
        
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
        
            
        