import customtkinter as ctk
import tkinter as tk
import secrets
from pynput import keyboard
from config_handler import ConfigHandler
from sound_player import SoundPlayer
from history_handler import HistoryHandler
import datetime
        
# GUI Class
class RngGui(ctk.CTk) :
    
    def __init__(self, config_handler, sound_player, history_handler) :
        super().__init__()
        
        # Config Handler
        self.config_handler : ConfigHandler = config_handler
        
        # Config Files
        self.cfg_style = self.config_handler.style_config
        self.cfg_hotkeys = self.config_handler.hotkeys_config
        self.cfg_preset = self.config_handler.preset_config
        
        # Sound Player
        self.sound_player : SoundPlayer = sound_player
        
        # History Handler
        self.history_handler : HistoryHandler = history_handler
        
        self.min_width = 300
        self.min_height = 340
        self.calc_width = self.min_width + self.min_width * self.cfg_preset["history"]
        
        # Full Container
        self.frame_container = ctk.CTkFrame(self, width=self.min_width, height=self.min_height)
        self.frame_container.pack(side="top", fill="both", expand=True)
        
        # Main Frame
        self.frame_main = ctk.CTkFrame(self.frame_container, width=self.min_width, height=self.min_height)
        self.frame_main.pack(side="left", fill="both", expand=True)
        
        # History Frame
        self.frame_history = ctk.CTkFrame(self.frame_container, width=self.min_width)
        self.frame_history.pack(side="left", fill="both", expand=True)
        
        # Root Window
        self.title("Random Number Generator by 8-Bit Hero")
        self.geometry(f"{self.calc_width}x{self.min_height}")
        self.minsize(self.min_width, self.min_height)
        
        # Menubar
        self.menubar = tk.Menu(self)
        
        # Sound Menu
        self.menu_sound = tk.Menu(self.menubar, tearoff=False)
        self.menu_sound.add_command(label='Enable/Disable Sound', command=self.sound_player.enable_disable_sound)
        self.menu_sound.add_command(label="Enable/Disable TTS", command=self.sound_player.enable_disable_tts)
        
        self.menubar.add_cascade(label="Sound", menu=self.menu_sound)
        
        # History Menu
        self.menu_history = tk.Menu(self.menubar, tearoff=False)
        self.menu_history.add_command(label="Enable/Disable History Tab", command=self.enable_disable_history_tab)
        
        self.menubar.add_cascade(label="History", menu=self.menu_history)
        
        self.config(menu=self.menubar)
        
        # Main Frame Contents
        self.frame_inputs = ctk.CTkFrame(self.frame_main)
        self.frame_inputs.pack(side="top", fill="both", expand=False)
        self.frame_inputs.columnconfigure(1, weight=1)
        
        self.frame_buttons = ctk.CTkFrame(self.frame_main)
        self.frame_buttons.pack(side="top", fill="both", expand=False)
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)
        
        self.frame_output = ctk.CTkScrollableFrame(self.frame_main)
        self.frame_output.pack(padx=10, pady=5, fill="both", expand="yes")
        
        # History Frame Contents
        self.lbl_history = ctk.CTkLabel(self.frame_history, text="Roll History")
        self.lbl_history.pack(padx=10, pady=5, fill="both", expand="no")
        
        self.lbl_history_headers = ctk.CTkLabel(self.frame_history, text="(Numbers, Min, Max, Time - Date)")
        self.lbl_history_headers.pack(padx=10, fill="both", expand="no")
        
        self.frame_inner_history = ctk.CTkFrame(self.frame_history)
        self.frame_inner_history.pack(side="top", fill="both", expand=True)
        
        self.textbox_history = ctk.CTkTextbox(self.frame_inner_history, activate_scrollbars=False, state="disabled", wrap="none")
        self.textbox_history.pack(padx=10, pady=5, fill="both", expand="yes")
        
        self.scrollbar_history_v = ctk.CTkScrollbar(self.frame_inner_history, orientation="vertical", command=self.textbox_history.yview)
        self.scrollbar_history_v.place(relx=1, rely=0, anchor="ne", relheight=1)
        self.scrollbar_history_h = ctk.CTkScrollbar(self.frame_inner_history, orientation="horizontal", command=self.textbox_history.xview)
        self.scrollbar_history_h.place(relx=1, rely=1, anchor="se", relwidth=1)
        
        self.textbox_history.configure(yscrollcommand=self.scrollbar_history_v.set, xscrollcommand=self.scrollbar_history_h.set)
        
        # variables to store values
        self.var_btwn = ctk.StringVar(self, value=self.cfg_preset["min"] or "1")
        self.var_and = ctk.StringVar(self, value=self.cfg_preset["max"] or "2")
        self.var_amount = ctk.StringVar(self, value=self.cfg_preset["amount"] or "2")
        self.var_output = ctk.StringVar(self, value="")
        self.var_history_active = ctk.BooleanVar(self, value=self.cfg_preset["history"] or True)
        
        # track variables
        self.var_btwn.trace_add("write", self.write_number_field)
        self.var_and.trace_add("write", self.write_number_field)
        self.var_amount.trace_add("write", self.write_number_field)
        
        # Labels and input fields
        self.lbl_btwn = ctk.CTkLabel(self.frame_inputs, text="Min")
        self.lbl_btwn.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_btwn = ctk.CTkEntry(self.frame_inputs, textvariable=self.var_btwn)
        self.entry_btwn.grid(row=0, column=1, padx=10, pady=5, sticky="EW")
        
        self.lbl_and = ctk.CTkLabel(self.frame_inputs, text="Max")
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
        
        # Output Label
        self.lbl_output = ctk.CTkLabel(self.frame_output, textvariable=self.var_output, anchor=ctk.N)
        self.lbl_output.pack()
        
        # Hotkeys
        self.hotkeys = keyboard.GlobalHotKeys({
            self.cfg_hotkeys["roll_single"] or None : self.hotkey_single,
            self.cfg_hotkeys["roll_multiple"] or None : self.hotkey_multiple,
            self.cfg_hotkeys["roll_d10"] or None : lambda : self.roll_predetermined(10),
            self.cfg_hotkeys["roll_d2"] or None : lambda : self.roll_predetermined(2),
            self.cfg_hotkeys["roll_d3"] or None : lambda : self.roll_predetermined(3),
            self.cfg_hotkeys["roll_d4"] or None : lambda : self.roll_predetermined(4),
            self.cfg_hotkeys["roll_d5"] or None : lambda : self.roll_predetermined(5),
            self.cfg_hotkeys["roll_d6"] or None : lambda : self.roll_predetermined(6),
            self.cfg_hotkeys["roll_d7"] or None : lambda : self.roll_predetermined(7),
            self.cfg_hotkeys["roll_d8"] or None : lambda : self.roll_predetermined(8),
            self.cfg_hotkeys["roll_d9"] or None : lambda : self.roll_predetermined(9)
            })
        self.hotkeys.start()
        
        # Style
        self.stylize(config_handler=config_handler)
        
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
            self.var_amount.set(''.join([x for x in self.var_amount.get() if x in valid_inputs[1:]]))
            
        # Save
        self.config_handler.preset_config["min"] = self.var_btwn.get()
        self.config_handler.preset_config["max"] = self.var_and.get()
        self.config_handler.preset_config["amount"] = self.var_amount.get()
            
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
        
        # Play tts
        self.sound_player.play_external_sound(output)
        
        # Record History
        self.history_handler.record(output, start, end)
        
        # Update History GUI
        self.textbox_history.configure(state="normal")
        self.textbox_history.insert(index=tk.END, text=f"{output}, {start}, {end}, {datetime.datetime.now().strftime('%X')} - {datetime.datetime.now().strftime('%x')}\n")
        self.textbox_history.configure(state="disabled")
        
        self.textbox_history.yview_moveto(1.0)
        
        return output
    
    def generate_multiple(self) :
        # get values from fields
        start = int(self.var_btwn.get() or "0")
        end = int(self.var_and.get() or "0")
        amount = 1 if self.var_amount.get() in ["", "0"] else int(self.var_amount.get())
        
        # Swap if min > max
        if start > end :
            start, end = end, start
        
        range_size = end - start + 1
        
        # prepare a list to store values
        output_list = [start + secrets.randbelow(range_size) for _ in range(min(300, amount))]
        
        # Add a space after every element
        formatted_list = "  ".join(str(num) for num in output_list)
        
        # fill the label field
        self.var_output.set(formatted_list)
        
        # play sound 
        self.sound_player.play_sound("roll_multiple")
        
        # Record History
        self.history_handler.record(formatted_list, start, end)
        
        # Update History GUI
        self.textbox_history.configure(state="normal")
        self.textbox_history.insert(index=tk.END, text=f"{formatted_list}, {start}, {end}, {datetime.datetime.now().strftime('%X')} - {datetime.datetime.now().strftime('%x')}\n")
        self.textbox_history.configure(state="disabled")
        
        self.textbox_history.yview_moveto(1.0)
        
        # arrange wraplength based on window width
        width = self.frame_output.winfo_width()
        self.lbl_output.configure(wraplength=width)
        
    def roll_predetermined(self, max) :
        # Roll
        random = secrets.randbelow(max) + 1
        
        # Update the output
        self.var_output.set(f"{random} (D{max})")
        
        # Play sound 
        self.sound_player.play_sound("roll_single")
        
        # Create and play TTS
        self.sound_player.play_external_sound(random)
        
        # Record History
        self.history_handler.record(random, 1, max)
        
        # Update History GUI
        self.textbox_history.configure(state="normal")
        self.textbox_history.insert(index=tk.END, text=f"{random}, {1}, {max}, {datetime.datetime.now().strftime('%X')} - {datetime.datetime.now().strftime('%x')}\n")
        self.textbox_history.configure(state="disabled")
        
        self.textbox_history.yview_moveto(1.0)
        
    def hotkey_single(self) :
        self.after(0, self.generate_single)
        
    def hotkey_multiple(self) :
        self.after(0, self.generate_multiple)
        
    def save(self) :
        self.config_handler.save_configs()
        self.destroy()
        
    def enable_disable_history_tab(self) :
        if self.var_history_active.get() :
            self.frame_history.forget()
        else :
            self.frame_history.pack(side="left", fill="both", expand=True)
        self.var_history_active.set(not self.var_history_active.get())
        self.config_handler.preset_config["history"] = self.var_history_active.get()
        
        # Resize
        self.calc_width = self.min_width + self.min_width * self.cfg_preset["history"]
        self.geometry(f"{self.calc_width}x{self.min_height}")
        print(self.calc_width)
            
    def stylize(self, config_handler : ConfigHandler) :
        # create font
        self.label_font = ctk.CTkFont(family=config_handler.style_config["label_font_family"], size=config_handler.style_config["label_font_size"], weight=config_handler.style_config["label_font_weight"])
        self.entry_font = ctk.CTkFont(family=config_handler.style_config["entry_font_family"], size=config_handler.style_config["entry_font_size"], weight=config_handler.style_config["entry_font_weight"])
        self.button_font = ctk.CTkFont(family=config_handler.style_config["button_font_family"], size=config_handler.style_config["button_font_size"], weight=config_handler.style_config["button_font_weight"])
        self.output_font = ctk.CTkFont(family=config_handler.style_config["output_font_family"], size=config_handler.style_config["output_font_size"], weight=config_handler.style_config["output_font_weight"])
        self.history_font = ctk.CTkFont(family=config_handler.style_config["history_font_family"], size=config_handler.style_config["history_font_size"], weight=config_handler.style_config["history_font_weight"])
        
        # Label Styling
        self.lbl_btwn.configure(font=self.label_font)
        self.lbl_and.configure(font=self.label_font)
        self.lbl_amount.configure(font=self.label_font)
        self.lbl_history.configure(font=self.label_font)
        
        # Entry Styling
        self.entry_btwn.configure(font=self.entry_font)
        self.entry_and.configure(font=self.entry_font)
        self.entry_amount.configure(font=self.entry_font)
        
        # Button Styling
        self.btn_single.configure(font=self.button_font, fg_color=config_handler.style_config["button_foreground_color"], hover_color=config_handler.style_config["button_hover_color"])
        self.btn_multiple.configure(font=self.button_font, fg_color=config_handler.style_config["button_foreground_color"], hover_color=config_handler.style_config["button_hover_color"])
        
        # Output Styling
        self.lbl_output.configure(font=self.output_font)
        
        # History Textbox Styling
        self.textbox_history.configure(font=self.history_font)
                    
if __name__ == '__main__' :
    # Call the Config Handler Class
    config_handler = ConfigHandler()
    
    # Call the Sound Player Class
    sound_player = SoundPlayer(config_handler=config_handler)
    
    # Initialize History Handler
    history_handler = HistoryHandler()
    
    # Call the GUI class
    gui = RngGui(config_handler=config_handler, sound_player=sound_player, history_handler=history_handler)
    gui.mainloop()