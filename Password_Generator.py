import random
import string
import tkinter as tk
from tkinter import messagebox


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Digital Key Smith")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e")  # Dark tech background
        self.root.resizable(False, False)

        # Default Configuration States
        self.password_length = 12
        self.include_uppercase = True
        self.include_numbers = True
        self.include_symbols = True

        # ---- 1. DIGITAL DISPLAY SCREEN ----
        self.display_frame = tk.Frame(root, bg="#11111b", bd=2, relief="solid")
        self.display_frame.pack(fill="x", padx=20, pady=20)

        # Main password output display
        self.password_display = tk.Entry(
            self.display_frame,
            font=("Consolas", 16, "bold"),
            fg="#fab387",  # Digital amber/orange readout
            bg="#11111b",
            bd=0,
            justify="center",
            insertbackground="#fab387",
        )
        self.password_display.pack(fill="x", padx=15, pady=(15, 5))
        self.password_display.insert(0, "CLICK GENERATE")

        # Live telemetry/status label beneath the password
        self.status_label = tk.Label(
            self.display_frame,
            text="LEN: 12 | UPPER: ON | NUM: ON | SYM: ON",
            font=("Consolas", 10),
            fg="#a6e3a1",  # Terminal green matrix text
            bg="#11111b",
            pady=5,
        )
        self.status_label.pack(fill="x")

        # ---- 2. INTERACTIVE GRID OF KEYS ----
        # A 3x3 layout housing parameters, rules, and action matrix triggers
        self.grid_frame = tk.Frame(root, bg="#1e1e2e")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Enforce symmetrical scaling for 3 columns and 3 rows
        for i in range(3):
            self.grid_frame.columnconfigure(i, weight=1)
            self.grid_frame.rowconfigure(i, weight=1)

        # Define individual Grid Keys
        # Row 0: Length Adjustment Keys
        self.btn_len_down = tk.Button(
            self.grid_frame,
            text="LEN -",
            font=("Segoe UI Black", 10),
            bg="#313244",
            fg="#cdd6f4",
            bd=0,
            command=self.decrease_length,
        )
        self.btn_len_down.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        self.btn_len_val = tk.Button(
            self.grid_frame,
            text="⚡ LEN: 12",
            font=("Segoe UI Black", 10),
            bg="#45475a",
            fg="#cdd6f4",
            bd=0,
            state="disabled",
            disabledforeground="#cdd6f4",
        )
        self.btn_len_val.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        self.btn_len_up = tk.Button(
            self.grid_frame,
            text="LEN +",
            font=("Segoe UI Black", 10),
            bg="#313244",
            fg="#cdd6f4",
            bd=0,
            command=self.increase_length,
        )
        self.btn_len_up.grid(row=0, column=2, padx=4, pady=4, sticky="nsew")

        # Row 1: Character Filter Toggle Keys
        self.btn_upper = tk.Button(
            self.grid_frame,
            text="[A-Z]\nON",
            font=("Segoe UI Black", 10),
            bg="#a6e3a1",
            fg="#11111b",
            bd=0,
            command=self.toggle_uppercase,
        )
        self.btn_upper.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

        self.btn_numbers = tk.Button(
            self.grid_frame,
            text="[0-9]\nON",
            font=("Segoe UI Black", 10),
            bg="#a6e3a1",
            fg="#11111b",
            bd=0,
            command=self.toggle_numbers,
        )
        self.btn_numbers.grid(row=1, column=1, padx=4, pady=4, sticky="nsew")

        self.btn_symbols = tk.Button(
            self.grid_frame,
            text="[!@#]\nON",
            font=("Segoe UI Black", 10),
            bg="#a6e3a1",
            fg="#11111b",
            bd=0,
            command=self.toggle_symbols,
        )
        self.btn_symbols.grid(row=1, column=2, padx=4, pady=4, sticky="nsew")

        # Row 2: Heavyweight Core Actions
        self.btn_copy = tk.Button(
            self.grid_frame,
            text="📋 COPY",
            font=("Segoe UI Black", 11),
            bg="#f9e2af",
            fg="#11111b",
            bd=0,
            command=self.copy_to_clipboard,
        )
        self.btn_copy.grid(
            row=2, column=0, columnspan=1, padx=4, pady=4, sticky="nsew"
        )

        self.btn_generate = tk.Button(
            self.grid_frame,
            text="🧱 GENERATE KEY",
            font=("Segoe UI Black", 11),
            bg="#89b4fa",
            fg="#11111b",
            bd=0,
            command=self.generate_password,
        )
        self.btn_generate.grid(
            row=2, column=1, columnspan=2, padx=4, pady=4, sticky="nsew"
        )

        # Apply basic hover cursor to everything clickable
        for child in self.grid_frame.winfo_children():
            if isinstance(child, tk.Button) and child != self.btn_len_val:
                child.config(cursor="hand2")

    # ---- RUNTIME FUNCTIONALITY ----

    def update_telemetry_display(self):
        # Update center structural indicator button
        self.btn_len_val.config(text=f"⚡ LEN: {self.password_length}")

        # Map logic flags to display texts
        up_status = "ON" if self.include_uppercase else "OFF"
        num_status = "ON" if self.include_numbers else "OFF"
        sym_status = "ON" if self.include_symbols else "OFF"

        # Push formatted updates directly to the LCD screen sub-label
        self.status_label.config(
            text=f"LEN: {self.password_length} | UPPER: {up_status} | NUM: {num_status} | SYM: {sym_status}"
        )

    def decrease_length(self):
        if self.password_length > 6:  # Safety floor for minimum secure length
            self.password_length -= 1
            self.update_telemetry_display()

    def increase_length(self):
        if self.password_length < 32:  # Ceiling cap to preserve GUI alignment bounds
            self.password_length += 1
            self.update_telemetry_display()

    def toggle_uppercase(self):
        self.include_uppercase = not self.include_uppercase
        self.btn_upper.config(
            bg="#a6e3a1" if self.include_uppercase else "#f38ba8",
            text=f"[A-Z]\n{'ON' if self.include_uppercase else 'OFF'}",
        )
        self.update_telemetry_display()

    def toggle_numbers(self):
        self.include_numbers = not self.include_numbers
        self.btn_numbers.config(
            bg="#a6e3a1" if self.include_numbers else "#f38ba8",
            text=f"[0-9]\n{'ON' if self.include_numbers else 'OFF'}",
        )
        self.update_telemetry_display()

    def toggle_symbols(self):
        self.include_symbols = not self.include_symbols
        self.btn_symbols.config(
            bg="#a6e3a1" if self.include_symbols else "#f38ba8",
            text=f"[!@#]\n{'ON' if self.include_symbols else 'OFF'}",
        )
        self.update_telemetry_display()

    def generate_password(self):
        # Core pool compilation begins with standard lowercase letters
        char_pool = string.ascii_lowercase

        if self.include_uppercase:
            char_pool += string.ascii_uppercase
        if self.include_numbers:
            char_pool += string.digits
        if self.include_symbols:
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # If zero parameters are selected, throw an alert
        if not any(
            [
                self.include_uppercase,
                self.include_numbers,
                self.include_symbols,
                char_pool,
            ]
        ):
            messagebox.showwarning(
                "Filter Error", "Please turn on at least one character set."
            )
            return

        # Secure selection algorithm
        generated_pwd = "".join(
            random.choice(char_pool) for _ in range(self.password_length)
        )

        # Render string into digital entry screen
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, generated_pwd)

    def copy_to_clipboard(self):
        current_pwd = self.password_display.get()
        if current_pwd and current_pwd != "CLICK GENERATE":
            self.root.clipboard_clear()
            self.root.clipboard_append(current_pwd)
            messagebox.showinfo(
                "Success", "Password securely copied to clipboard!"
            )
        else:
            messagebox.showwarning(
                "Empty Matrix", "Nothing to copy yet. Generate a password first."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()