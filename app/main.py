import customtkinter as ctk
import tkinter as tk
import secrets
from pynput import keyboard
from config_handler import ConfigHandler
from cache_handler import CacheHandler
from sound_player import SoundPlayer
import os
import json
        
# GUI Class
class RngGui(ctk.CTk) :
    
    def __init__(self, config_handler, cache_handler, sound_player) :
        super().__init__()
        
        # Config Handler
        self.config_handler : ConfigHandler = config_handler
        
        # Config files
        self.cfg_style = self.config_handler.style_config
        self.cfg_hotkeys = self.config_handler.hotkeys_config
        
        # Cache Handler
        self.cache_handler : CacheHandler = cache_handler
        
        # Cache
        self.cache = cache_handler.cache
        
        # Sound Player
        self.sound_player : SoundPlayer = sound_player
        
        # root window
        self.title("Random Number Generator by 8-Bit Hero")
        self.geometry("300x300")
        self.minsize(300, 300)
        
        # Menubar
        self.menubar = tk.Menu(self)
        
        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        
        self.menubar.add_cascade(label="File", menu=self.menu_file)
        
        self.config(menu=self.menubar)
        
        # frame to store labels, inputs and/or buttons
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.pack(side="top", fill="both", expand=False)
        
        self.frame_inputs.columnconfigure(1, weight=1)
        
        self.frame_buttons = ctk.CTkFrame(self)
        self.frame_buttons.pack(side="top", fill="both", expand=False)
        
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)
        
        self.frame_output = ctk.CTkFrame(self)
        self.frame_output.pack(padx=10, pady=5, fill="both", expand="yes")
        
        # variables to store values
        self.var_btwn = ctk.StringVar(self, value=self.cache["between"] or "1")
        self.var_and = ctk.StringVar(self, value=self.cache["and"] or "2")
        self.var_amount = ctk.StringVar(self, value=self.cache["amount"] or "2")
        self.var_output = ctk.StringVar(self, value="")
        
        # track variables
        self.var_btwn.trace_add("write", self.write_number_field)
        self.var_and.trace_add("write", self.write_number_field)
        self.var_amount.trace_add("write", self.write_number_field)
        
        # between - and - amount labels and input fields
        self.lbl_btwn = ctk.CTkLabel(self.frame_inputs, text="Between")
        self.lbl_btwn.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_btwn = ctk.CTkEntry(self.frame_inputs, textvariable=self.var_btwn)
        self.entry_btwn.grid(row=0, column=1, padx=10, pady=5, sticky="EW")
        
        self.lbl_and = ctk.CTkLabel(self.frame_inputs, text="And")
        self.lbl_and.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_and = ctk.CTkEntry(self.frame_inputs, textvariable=self.var_and)
        self.entry_and.grid(row=1, column=1, padx=10, pady=5, sticky="EW")
        
        self.lbl_amount = ctk.CTkLabel(self.frame_inputs, text="Amount")
        self.lbl_amount.grid(row=2, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_amount = ctk.CTkEntry(self.frame_inputs, textvariable=self.var_amount)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=5, sticky="EW")
        
        # Buttons
        self.btn_single = ctk.CTkButton(self.frame_buttons, text="Roll Single", command=self.generate_single)
        self.btn_single.grid(row=0, column=0, padx=10, pady=8, sticky="WE")
        
        self.btn_multiple = ctk.CTkButton(self.frame_buttons, text="Roll Multiple", command=self.generate_multiple)
        self.btn_multiple.grid(row=0, column=1, padx=10, pady=8, sticky="WE")
        
        # Label
        self.lbl_output = ctk.CTkLabel(self.frame_output, textvariable=self.var_output)
        self.lbl_output.pack()
        
        # Hotkeys
        self.hotkeys = keyboard.GlobalHotKeys({
            self.cfg_hotkeys["roll_single"] or None : self.hotkey_single,
            self.cfg_hotkeys["roll_multiple"] or None : self.hotkey_multiple
            })
        self.hotkeys.start()
        
        # Override window destroy behavior
        self.protocol('WM_DELETE_WINDOW', self.save)
        
    def write_number_field(self, var, index, mode) :
        # Valid inputs list
        valid_inputs = ["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        # Check which field it is, then change the value based on valid inputs
        if var == str(self.var_btwn) :
            self.var_btwn.set(''.join([x for x in self.var_btwn.get() if x in valid_inputs]))
            if self.var_btwn.get().find("-", 1) >= 0 :
                self.var_btwn.set(self.var_btwn.get()[0] + self.var_btwn.get()[1:].replace("-", ""))
        elif var == str(self.var_and) :
            self.var_and.set(''.join([x for x in self.var_and.get() if x in valid_inputs]))
            if self.var_and.get().find("-", 1) >= 0 :
                self.var_and.set(self.var_and.get()[0] + self.var_and.get()[1:].replace("-", ""))
        elif var == str(self.var_amount) :
            self.var_amount.set(''.join([x for x in self.var_amount.get() if x in valid_inputs[2:]]))
            
    def generate_single(self) :
        # get values from fields
        start = int(self.var_btwn.get() or "0")
        end = int(self.var_and.get() or "0")
        
        # Swap if min > max
        if start > end :
            start, end = end, start
        
        range_size = end - start + 1
        random_offset = secrets.randbelow(range_size)
        output = start + random_offset
        
        self.var_output.set(output)
        
        # Play sound 
        self.sound_player.play_sound("roll_single")
        
        return output
    
    def generate_multiple(self) :
        # get values from fields
        start = int(self.var_btwn.get() or "0")
        end = int(self.var_and.get() or "0")
        amount = int(self.var_amount.get() or "1")
        
        # Swap if min > max
        if start > end :
            start, end = end, start
        
        range_size = end - start + 1
        
        # prepare a list to store values
        output_list = [start + secrets.randbelow(range_size) for _ in range(min(300, amount))]
        
        # fill the label field
        self.var_output.set(output_list)
        
        # play sound 
        self.sound_player.play_sound("roll_multiple")
        
        # arrange wraplength based on window width
        self.lbl_output.configure(wraplength=self.winfo_width() - 30)
        
    def hotkey_single(self) :
        self.after(0, self.generate_single)
        
    def hotkey_multiple(self) :
        self.after(0, self.generate_multiple)
        
    def save(self) :
        if os.path.exists(self.cache_handler.cache_path):
            with open(self.cache_handler.cache_path, "r") as f:
                cache = json.load(f)
                cache["between"] = self.var_btwn.get() or "1"
                cache["and"] = self.var_and.get() or "2"
                cache["amount"] = self.var_amount.get() or "2"
                
        with open(self.cache_handler.cache_path, "w+") as f:
            json.dump(cache, f, indent=4)
        self.destroy()
    
                    
if __name__ == '__main__' :
    # Call the Config Handler Class
    config_handler = ConfigHandler()
    
    # Call the Cache Class
    cache_handler = CacheHandler()
    
    # Call the Sound Player Class
    sound_player = SoundPlayer(config_handler=config_handler)
    
    # Call the GUI class
    gui = RngGui(config_handler=config_handler, cache_handler=cache_handler, sound_player=sound_player)
    gui.mainloop()