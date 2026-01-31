import tkinter as tk

# GUI Class
class Rng_GUI :
    
    def __init__(self) :
        # root window
        self.root = tk.Tk()
        self.root.title("Random Number Generator by 8-Bit Hero")
        self.root.geometry("300x300")
        self.root.minsize(300, 300)
        self.root.maxsize(300, 300)
        
        # frame to store labels and inputs
        self.frame_inputs = tk.Frame(self.root)
        self.frame_inputs.pack(side="top", fill="both", expand=False)
        
        self.frame_inputs.columnconfigure(1, weight=1)
        
        # variables to store values
        self.var_btwn = tk.StringVar(self.root, value="1")
        self.var_and = tk.StringVar(self.root, value="2")
        self.var_amount = tk.StringVar(self.root, value="2")
        
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
            self.var_amount.set(''.join([x for x in self.var_amount.get() if x in valid_inputs[1:]]))
            
            
# Call the class
Rng_GUI()