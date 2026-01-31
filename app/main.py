import tkinter as tk
import secrets
import pygame


# GUI Class
class Rng_GUI :
    
    def __init__(self) :
        # root window
        self.root = tk.Tk()
        self.root.title("Random Number Generator by 8-Bit Hero")
        self.root.geometry("300x300")
        self.root.minsize(300, 300)
        
        # frame to store labels, inputs and/or buttons
        self.frame_inputs = tk.Frame(self.root)
        self.frame_inputs.pack(side="top", fill="both", expand=False)
        
        self.frame_inputs.columnconfigure(1, weight=1)
        
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(side="top", fill="both", expand=False)
        
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)
        
        self.frame_output = tk.LabelFrame(self.root, text="Outputs")
        self.frame_output.pack(padx=10, pady=5, fill="both", expand="yes")
        
        # variables to store values
        self.var_btwn = tk.StringVar(self.root, value="1")
        self.var_and = tk.StringVar(self.root, value="2")
        self.var_amount = tk.StringVar(self.root, value="2")
        self.var_output = tk.StringVar(self.root, value="")
        
        # track variables
        self.var_btwn.trace_add("write", self.write_number_field)
        self.var_and.trace_add("write", self.write_number_field)
        self.var_amount.trace_add("write", self.write_number_field)
        
        # between - and - amount labels and input fields
        self.lbl_btwn = tk.Label(self.frame_inputs, text="Between")
        self.lbl_btwn.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_btwn = tk.Entry(self.frame_inputs, textvariable=self.var_btwn)
        self.entry_btwn.grid(row=0, column=1, padx=10, pady=5, sticky="EW")
        
        self.lbl_and = tk.Label(self.frame_inputs, text="To")
        self.lbl_and.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_and = tk.Entry(self.frame_inputs, textvariable=self.var_and)
        self.entry_and.grid(row=1, column=1, padx=10, pady=5, sticky="EW")
        
        self.lbl_amount = tk.Label(self.frame_inputs, text="Amount")
        self.lbl_amount.grid(row=2, column=0, padx=10, pady=5, sticky="W")
        
        self.entry_amount = tk.Entry(self.frame_inputs, textvariable=self.var_amount)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=5, sticky="EW")
        
        # Buttons
        self.btn_single = tk.Button(self.frame_buttons, text="Roll Single", command=self.generate_single)
        self.btn_single.grid(row=0, column=0, padx=10, pady=8, sticky="WE")
        
        self.btn_multiple = tk.Button(self.frame_buttons, text="Roll Multiple", command=self.generate_multiple)
        self.btn_multiple.grid(row=0, column=1, padx=10, pady=8, sticky="WE")
        
        # Label
        self.lbl_output = tk.Label(self.frame_output, textvariable=self.var_output)
        self.lbl_output.pack()
        
        # Hotkeys
        self.root.bind("<Control-KeyPress-1>", self.generate_single_hotkey)
        self.root.bind("<Control-KeyPress-2>", self.generate_multiple_hotkey)
        
        # Pygame sound
        pygame.mixer.init()
        
        # Infinite loop for the window to stay open
        self.root.mainloop()
        
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
        start = int(self.var_btwn.get())
        end = int(self.var_and.get())
        
        # Swap if min > max
        if start > end :
            start, end = end, start
        
        range_size = end - start + 1
        random_offset = secrets.randbelow(range_size)
        output = start + random_offset
        
        self.var_output.set(output)
        
        # Play sound 
        self.play_sound("resources/sfx/dice_roll.wav")
        
        return output
    
    def generate_multiple(self) :
        # get values from fields
        amount = max(1, int(self.var_amount.get()))
        
        # prepare a list to store values
        output_list = []
        
        # call generate method
        for i in range(min(300, amount)) :
            output_list.append(self.generate_single())
        
        # fill the label field
        self.var_output.set(output_list)
        
        # reset the list
        output_list.clear()
        
        # arrange wraplength based on window width
        self.lbl_output.configure(wraplength=self.root.winfo_width() - 30)
        
    def generate_single_hotkey(self, e) :
        self.generate_single()
        
    def generate_multiple_hotkey(self, e) :
        self.generate_multiple()
        
    def play_sound(self, path) :
        sound = pygame.mixer.Sound(path)
        sound.play()
        sound.set_volume(0.05)
            
if __name__ == '__main__' :
    # Call the class
    Rng_GUI()