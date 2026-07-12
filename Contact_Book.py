import tkinter as tk
from tkinter import messagebox, ttk

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Contact Book")
        self.root.geometry("850x550")
        self.root.config(bg="#f4f6f9")

        # Empty database - starts completely blank as requested
        self.contacts = []
        
        # Track sorting state and currently selected contact index
        self.sort_reverse = False
        self.selected_contact_idx = None 
        
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # --- TOP SECTION: Search Bar ---
        search_frame = tk.Frame(self.root, bg="#f4f6f9")
        search_frame.pack(fill="x", padx=15, pady=10)

        search_lbl = tk.Label(search_frame, text="Search (Name/Phone):", bg="#f4f6f9", font=("Arial", 10, "bold"))
        search_lbl.pack(side="left", padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_table())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, font=("Arial", 10))
        search_entry.pack(side="left", padx=5)

        # --- MIDDLE SECTION: Input Form ---
        self.form_frame = tk.LabelFrame(self.root, text=" Contact Details ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=10, pady=10)
        self.form_frame.pack(fill="x", padx=15, pady=5)

        fields = ["Name", "Phone", "Email", "Address"]
        self.entries = {}

        for i, field in enumerate(fields):
            lbl = tk.Label(self.form_frame, text=f"{field}:", bg="#f4f6f9", font=("Arial", 9, "bold"))
            lbl.grid(row=0, column=i*2, padx=5, pady=5, sticky="e")
            
            entry = tk.Entry(self.form_frame, width=15, font=("Arial", 10))
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.entries[field] = entry

        # --- BUTTONS SECTION: CRUD Actions ---
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.add_btn = tk.Button(btn_frame, text="➕ Add & Save", command=self.add_contact, bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10, pady=5)
        self.add_btn.pack(side="left", padx=5)

        self.update_btn = tk.Button(btn_frame, text="🔄 Update Selected", command=self.update_contact, bg="#3498db", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10, pady=5, state="disabled")
        self.update_btn.pack(side="left", padx=5)

        self.clear_btn = tk.Button(btn_frame, text="🧹 Clear Form", command=self.clear_form, bg="#95a5a6", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10, pady=5)
        self.clear_btn.pack(side="left", padx=5)

        self.del_btn = tk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_contact, bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=10, pady=5, state="disabled")
        self.del_btn.pack(side="right", padx=5)

        # --- BOTTOM SECTION: Data Table ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        # Table Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#2c3e50", foreground="white")
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.map("Treeview.Heading", background=[('active', '#1a252f')])

        # Clickable Header Sort Configuration
        for col in columns:
            self.tree.heading(col, text=f"{col} ↕", command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Event binding for row selection
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # --- FUNCTIONALITY METHODS ---

    def refresh_table(self):
        """Clears and re-populates the table view based on search query."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_query = self.search_var.get().lower()

        for contact in self.contacts:
            # Filter results if search bar has text
            if search_query in contact["Name"].lower() or search_query in contact["Phone"]:
                self.tree.insert("", "end", values=(contact["Name"], contact["Phone"], contact["Email"], contact["Address"]))

    def on_row_select(self, event):
        """Triggers when a user clicks a row. Fills out form fields for modification."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item)["values"]
        
        # Populate the entry boxes
        for i, field in enumerate(["Name", "Phone", "Email", "Address"]):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, row_values[i])

        # Track internal index of selected contact
        for idx, contact in enumerate(self.contacts):
            if contact["Name"] == row_values[0] and contact["Phone"] == str(row_values[1]):
                self.selected_contact_idx = idx
                break

        # Adjust Button States
        self.update_btn.config(state="normal")
        self.del_btn.config(state="normal")
        self.add_btn.config(state="disabled")

    def add_contact(self):
        """Appends a unique new contact."""
        name = self.entries["Name"].get().strip()
        phone = self.entries["Phone"].get().strip()
        email = self.entries["Email"].get().strip()
        address = self.entries["Address"].get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone fields are required!")
            return

        # Check for duplicates
        if any(c["Phone"] == phone for c in self.contacts):
            messagebox.showerror("Error", "A contact with this phone number already exists.")
            return

        self.contacts.append({"Name": name, "Phone": phone, "Email": email, "Address": address})
        self.refresh_table()
        self.clear_form()

    def update_contact(self):
        """Modifies the values of the selected contact database index."""
        if self.selected_contact_idx is None:
            return

        name = self.entries["Name"].get().strip()
        phone = self.entries["Phone"].get().strip()
        email = self.entries["Email"].get().strip()
        address = self.entries["Address"].get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone cannot be blank!")
            return

        # Commit updates
        self.contacts[self.selected_contact_idx] = {"Name": name, "Phone": phone, "Email": email, "Address": address}
        
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        """Removes the selected contact index from dataset."""
        if self.selected_contact_idx is not None:
            del self.contacts[self.selected_contact_idx]
            self.refresh_table()
            self.clear_form()

    def clear_form(self):
        """Resets the UI form status back to baseline operational entry state."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_contact_idx = None
        self.update_btn.config(state="disabled")
        self.del_btn.config(state="disabled")
        self.add_btn.config(state="normal")
        self.tree.selection_remove(self.tree.selection())

    def sort_by_column(self, col):
        """Sorts contact records alphabetically dynamically by key clicks."""
        self.sort_reverse = not self.sort_reverse
        self.contacts.sort(key=lambda x: x[col].lower(), reverse=self.sort_reverse)
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()