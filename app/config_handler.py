import json
import os

# Config Handler Class
class ConfigHandler() :    
    
    def __init__(self) :
        self.base_directory = "config/"
        
        self.preset_config_path = self.base_directory + "preset.json"
        self.style_config_path = self.base_directory + "style.json"
        self.hotkeys_config_path = self.base_directory + "hotkeys.json"
        self.sfx_config_path = self.base_directory + "sfx.json"
        self.sound_config_path = self.base_directory + "sound.json"
        
        self.default_preset_config = {"min": "1", "max": "2", "amount": "2"}
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
        self.default_sound_config = {"sound_enabled" : True, "tts_enabled" : True}
        
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
        
            
        