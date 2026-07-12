import tkinter as tk
from tkinter import messagebox, ttk


class TodoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Digital Task Manager")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e")  # Dark modern background
        self.root.resizable(False, False)

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure custom scrollbar to match dark theme
        self.style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#313244",
            troughcolor="#1e1e2e",
            bordercolor="#1e1e2e",
            arrowcolor="#cdd6f4",
        )

        # ---- 1. DIGITAL DISPLAY HEADER ----
        self.display_frame = tk.Frame(root, bg="#11111b", bd=2, relief="solid")
        self.display_frame.pack(fill="x", padx=20, pady=15)

        self.stats_label = tk.Label(
            self.display_frame,
            text="TASKS: 0  |  COMPLETED: 0",
            font=("Consolas", 14, "bold"),
            fg="#a6e3a1",  # Digital green/mint text
            bg="#11111b",
            anchor="w",
            padx=15,
            pady=10,
        )
        self.stats_label.pack(fill="x")

        # ---- 2. INPUT SECTION ----
        self.input_frame = tk.Frame(root, bg="#1e1e2e")
        self.input_frame.pack(fill="x", padx=20, pady=5)

        self.task_entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 12),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            bd=0,
            highlightthickness=1,
            highlightbackground="#45475a",
            highlightcolor="#89b4fa",
        )
        # Subtle padding simulation inside Entry
        self.task_entry.pack(
            fill="x", ipady=8
        )  # ipady creates internal vertical padding
        self.task_entry.insert(0, "Type a new task here...")
        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
        self.task_entry.bind("<FocusOut>", self.add_placeholder)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # ---- 3. TASK LISTBOX VISUAL ----
        self.list_frame = tk.Frame(root, bg="#1e1e2e")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical")

        self.task_listbox = tk.Listbox(
            self.list_frame,
            font=("Segoe UI", 11),
            bg="#181825",
            fg="#cdd6f4",
            selectbackground="#b4befe",
            selectforeground="#11111b",
            activestyle="none",
            bd=0,
            highlightthickness=1,
            highlightbackground="#45475a",
            yscrollcommand=self.scrollbar.set,
        )

        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.task_listbox.pack(side="left", fill="both", expand=True)

        # ---- 4. INTERACTIVE GRID OF KEYS ----
        self.button_frame = tk.Frame(root, bg="#1e1e2e")
        self.button_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Configure 2x2 grid columns and rows evenly
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Custom button styles/configs using standard TK to allow easier hover colors
        btn_configs = [
            (
                "➕ ADD TASK",
                "#89b4fa",
                "#11111b",
                self.add_task,
                0,
                0,
            ),  # Text, BG, FG, Func, Row, Col
            ("✔️ COMPLETE", "#a6e3a1", "#11111b", self.complete_task, 0, 1),
            ("❌ DELETE", "#f38ba8", "#11111b", self.delete_task, 1, 0),
            ("🧹 CLEAR ALL", "#f9e2af", "#11111b", self.clear_all, 1, 1),
        ]

        for text, bg, fg, func, row, col in btn_configs:
            btn = tk.Button(
                self.button_frame,
                text=text,
                font=("Segoe UI Black", 10),
                bg=bg,
                fg=fg,
                activebackground=fg,
                activeforeground=bg,
                bd=0,
                pady=12,
                cursor="hand2",
                command=func,
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        # Internal tracking lists
        self.tasks = []
        self.completed_count = 0

    # ---- FUNCTIONALITY LOGIC ----
    def clear_placeholder(self, event):
        if self.task_entry.get() == "Type a new task here...":
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg="#cdd6f4")

    def add_placeholder(self, event):
        if not self.task_entry.get().strip():
            self.task_entry.insert(0, "Type a new task here...")
            self.task_entry.config(fg="#7f849c")

    def update_digital_display(self):
        total_tasks = len(self.tasks)
        self.stats_label.config(
            text=f"TASKS: {total_tasks}  |  COMPLETED: {self.completed_count}"
        )

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if (
            task_text
            and task_text != "Type a new task here..."
            and task_text != ""
        ):
            self.tasks.append(task_text)
            self.task_listbox.insert(tk.END, f" ▢  {task_text}")
            self.task_entry.delete(0, tk.END)
            self.update_digital_display()
        else:
            messagebox.showwarning("Empty Task", "Please enter a valid task.")

    def complete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            current_text = self.task_listbox.get(selected_index)

            # Check if it's already marked complete
            if "☑" not in current_text:
                clean_text = current_text.replace(" ▢  ", "")
                self.task_listbox.delete(selected_index)
                # Re-insert with a checked box visual
                self.task_listbox.insert(selected_index, f" ☑  {clean_text}")
                # Color the completed task slightly dimmer
                self.task_listbox.itemconfig(selected_index, fg="#585b70")

                self.completed_count += 1
                self.update_digital_display()
        except IndexError:
            messagebox.showwarning(
                "Selection Error", "Please select a task to mark complete."
            )

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            current_text = self.task_listbox.get(selected_index)

            # Adjust completion count if we delete an already completed task
            if "☑" in current_text:
                self.completed_count -= 1

            self.task_listbox.delete(selected_index)
            del self.tasks[selected_index]
            self.update_digital_display()
        except IndexError:
            messagebox.showwarning(
                "Selection Error", "Please select a task to delete."
            )

    def clear_all(self):
        if self.tasks:
            if messagebox.askyesno(
                "Clear All", "Are you sure you want to wipe the board?"
            ):
                self.task_listbox.delete(0, tk.END)
                self.tasks.clear()
                self.completed_count = 0
                self.update_digital_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()