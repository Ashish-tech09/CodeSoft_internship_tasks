import tkinter as tk

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("350x450")
        self.root.resizable(False, False)
        
        # String variable to track and display the math expression strings
        self.equation_text = ""
        self.display_var = tk.StringVar(value="0")

        # --- DISPLAY SCREEN ---
        # The window screen where the inputs and final outputs are displayed
        display_frame = tk.Frame(root, padx=10, pady=10)
        display_frame.pack(fill="x")

        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=("Helvetica", 24), 
            bg="#222222", 
            fg="#FFFFFF", 
            anchor="e", 
            padx=10, 
            pady=15
        )
        display_label.pack(fill="x")

        # --- BUTTON GRID FRAME ---
        btn_frame = tk.Frame(root, padx=10, pady=10)
        btn_frame.pack(fill="both", expand=True)

        # Configures grid weights so buttons scale to fill up the application area evenly
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        # Layout mapping out the calculator keypad coordinates
        buttons = [
            ('C', 0, 0), ('(', 0, 1), (')', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2)
        ]

        # Dynamically build and bind standard actions to key layout elements
        for (text, row, col) in buttons:
            action = lambda x=text: self.on_button_click(x)
            
            # Styling tweaks for system operations vs normal numbers
            if text == '=':
                btn = tk.Button(btn_frame, text=text, command=action, font=("Helvetica", 14), bg="#4CAF50", fg="white")
                # Make the "=" sign span across the final 2 column positions
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            elif text == 'C':
                btn = tk.Button(btn_frame, text=text, command=action, font=("Helvetica", 14), bg="#f44336", fg="white")
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            elif text in ['/', '*', '-', '+']:
                btn = tk.Button(btn_frame, text=text, command=action, font=("Helvetica", 14), bg="#FF9800", fg="white")
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            else:
                btn = tk.Button(btn_frame, text=text, command=action, font=("Helvetica", 14))
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, char):
        """Processes click coordinates and updates calculations."""
        if char == 'C':
            self.equation_text = ""
            self.display_var.set("0")
            
        elif char == '=':
            try:
                # Built-in eval processes arithmetic logic safely directly out of standard text strings
                result = str(eval(self.equation_text))
                self.display_var.set(result)
                # Keep the result active as the new baseline calculation string
                self.equation_text = result 
            except ZeroDivisionError:
                self.display_var.set("Error: Div by 0")
                self.equation_text = ""
            except Exception:
                self.display_var.set("Error")
                self.equation_text = ""
                
        else:
            self.equation_text += str(char)
            self.display_var.set(self.equation_text)

if __name__ == "__main__":
    window = tk.Tk()
    app = CalculatorGUI(window)
    window.mainloop()