import json
import os

style_config_path = "config/style.json"
hotkeys_config_path = "config/hotkeys.json"

# Config Handler Class
class ConfigHandler() :
    
    def __init__(self) :
        # Layout config
        if os.path.exists(style_config_path):
            with open(style_config_path) as f:
                self.style_config = json.load(f)
        
        # Hotkey config
        if os.path.exists(hotkeys_config_path):
            with open(hotkeys_config_path) as f:
                self.hotkeys_config = json.load(f)
            
        