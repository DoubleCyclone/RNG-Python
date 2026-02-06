import json
import os

# Config Handler Class
class ConfigHandler() :    
    
    def __init__(self) :
        self.base_directory = "config/"
        
        self.style_config_path = self.base_directory + "style.json"
        self.hotkeys_config_path = self.base_directory + "hotkeys.json"
        self.sfx_config_path = self.base_directory + "sfx.json"
        
        self.default_hotkeys_config = {
            "roll_single": "<alt>+q",
            "roll_multiple": "<alt>+w",
            "roll_d2": "<alt>+2",
            "roll_d3": "<alt>+3",
            "roll_d4": "<alt>+4",
            "roll_d5": "<alt>+5",
            "roll_d6": "<alt>+6",
            "roll_d7": "<alt>+7",
            "roll_d8": "<alt>+8",
            "roll_d9": "<alt>+9"
        }
        self.default_style_config = {
            "label_font_family" : "Roboto", "label_font_size" : 16, "label_font_weight" : "normal", "entry_font_family" : "Roboto", "entry_font_size" : 14,
            "entry_font_weight" : "normal", "button_font_family" : "Roboto",  "button_font_size" : 16, "button_font_weight" : "bold", "button_foreground_color" : "#663399",
            "button_hover_color" : "#4E2775", "output_font_family" : "Roboto",  "output_font_size" : 64, "output_font_weight" : "normal"
        }
        self.default_sfx_config = {"roll_single" : "resources/sfx/dice_roll.wav", "roll_multiple" : "resources/sfx/dice_roll.wav"}
        
        # Create base dir if does not exist
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)
        
        # Style config
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
        
            
        