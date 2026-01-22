from tkinter import *
import records
import users

class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("400x200")
        self.user=None

        # These will store the input values
        self.username = None
        self.password = None
        self.attempt = None
        self.first_name = None
        self.second_name = None 

    def clear_window(self):
        """Remove all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def setUser(self,user):
        self.user=user

    def populate_listbox(listbox, items):
        listbox.delete(0, END)
        for item in items:
            listbox.insert(END, item.display_record())

    def main_menu(self, warning_items, items,user):
        self.user=user
        self.clear_window()

        Label(self.root, text="Inventory", font=("Helvetica", 16)).pack(pady=10)

            # --- SEARCH CONTROLS ---
        search_frame = Frame(self.root)
        search_frame.pack(pady=5)

        field_var = StringVar(value="product_name")
        value_var = StringVar()

        OptionMenu(
            search_frame,
            field_var,
            "product_name",
            "Product_code",
            "quantity",
            "unit",
            "who"
        ).grid(row=0, column=0, padx=5)

        Entry(search_frame, textvariable=value_var, width=20).grid(row=0, column=1, padx=5)

               # --- SEARCH FUNCTION ---
        def search():
            feild = field_var.get()
            value = value_var.get()

            if value == "":
                populate(items)
                return

            results = records.Record_manager.search(feild, value, user)

            if results:
                populate(results)
            else:
                listbox.delete(0, END)
                listbox.insert(END, "No results found")


        Button(
            search_frame,
            text="Search",
            command=search
        ).grid(row=0, column=2, padx=5)

        Label(self.root, text="All Items").pack(pady=5)

        listbox = Listbox(self.root, width=60, height=12)
        listbox.pack(pady=5)

        
        self.current_items = items

        def populate(item_list):
            listbox.delete(0, END)
            self.current_items = item_list
            for item in item_list:
                listbox.insert(END, item.display_record())

        def populate_warning(item_list):
            Label(self.root, text="Warning: Low Stock Items", fg="red").pack()
            warning_listbox = Listbox(self.root, width=60, height=12)
            warning_listbox.pack(pady=5)
            warning_listbox.delete(0, END)
            self.warning_items = item_list
            for item in item_list:
                warning_listbox.insert(END, item.display_record())

        if warning_items:
            populate_warning(warning_items)
            populate(items)
        else:
            populate(items)

        def open_selected(event=None):
            if not listbox.curselection():
                return

            index = listbox.curselection()[0]
            record = self.current_items[index]
            self.item_menu(record)

        listbox.bind("<Double-Button-1>", open_selected)

        Button(
            self.root,
            text="Create New Item",
            command=self.create_item_menu
        ).pack(pady=5)

        self.root.mainloop()

    def create_item_menu(self):
        self.clear_window()

        Label(self.root, text="Create New Item", font=("Helvetica", 16)).pack(pady=10)

        name_var = StringVar()
        code_var = StringVar()
        qty_var = StringVar()
        unit_var = StringVar()

        
        Label(self.root, text="Product Name").pack()
        Entry(self.root, textvariable=name_var).pack()
        Label(self.root, text="Product Code").pack()
        Entry(self.root, textvariable=code_var).pack()
        Label(self.root, text="Quantity").pack()
        Entry(self.root, textvariable=qty_var).pack()
        Label(self.root, text="Unit").pack()
        Entry(self.root, textvariable=unit_var).pack()

        message = Label(self.root, fg="red")
        message.pack()


        def create():
            if not name_var.get():
                message.config(text="Name required")
                return

            if not code_var.get():
                message.config(text="Code required")
                return

            if not qty_var.get().isdigit():
                message.config(text="Quantity must be a number")
                return

            record = records.Record(
                name_var.get(),
                code_var.get(),
                self.user,
                int(qty_var.get()),
                unit_var.get()
            )

            record.write_record()
            self.refresh_main_menu()

        Button(self.root, text="Create", command=create).pack(pady=5)
        Button(self.root, text="Cancel", command=self.refresh_main_menu).pack(pady=5)


    def login_gui(self, issue):
        """Display the login screen and return (username, password, attempt=True)."""
        self.clear_window()

        Label(self.root, text="Login").grid(row=0, column=0, columnspan=2, pady=5)

        Label(self.root, text="Username:").grid(row=1, column=0, sticky=E)
        username_entry = Entry(self.root)
        username_entry.grid(row=1, column=1, pady=5)

        Label(self.root, text="Password:").grid(row=2, column=0, sticky=E)
        password_entry = Entry(self.root, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        if issue:
            Label(self.root, text="login failed: try again or sign up", fg="red").grid(row=4, column=0, columnspan=2)

        # Button functions
        def login():
            self.username = username_entry.get()
            self.password = password_entry.get()
            self.attempt = True  # login attempt
            self.root.quit()     # exit mainloop to return control

        def signup():
            self.username = username_entry.get()
            self.password = password_entry.get()
            self.attempt = False  # sign-up attempt
            self.root.quit()      # exit mainloop

        Button(self.root, text="Login", command=login, width=10).grid(row=3, column=0, pady=10)
        Button(self.root, text="Sign Up", command=signup, width=10).grid(row=3, column=1, pady=10)

        # Wait for user input
        self.root.mainloop()

        return self.username, self.password, self.attempt

    def signUp_gui(self):
        """Display the sign-up screen and return (username, password)."""
        self.clear_window()

        Label(self.root, text="Sign Up").grid(row=0, column=0, columnspan=2, pady=5)

        Label(self.root, text="first name:").grid(row=1, column=0, sticky=E)
        first_name_entry = Entry(self.root)
        first_name_entry.grid(row=1, column=1, pady=5)

        Label(self.root, text="second name:").grid(row=2, column=0, sticky=E)
        second_name_entry = Entry(self.root)
        second_name_entry.grid(row=2, column=1, pady=5)

        Label(self.root, text="Username:").grid(row=3, column=0, sticky=E)
        username_entry = Entry(self.root)
        username_entry.grid(row=3, column=1, pady=5)
        
        Label(self.root, text="Password:").grid(row=4, column=0, sticky=E)
        password_entry = Entry(self.root, show="*")
        password_entry.grid(row=4, column=1, pady=5)


        def signup():
            self.username = username_entry.get()
            self.password = password_entry.get()
            self.first_name = first_name_entry.get()
            self.second_name = second_name_entry.get()
            self.root.quit()  # exit mainloop

        Button(self.root, text="Sign Up", command=signup, width=15).grid(row=5, column=0, columnspan=2, pady=10)
        self.root.mainloop()

        return self.username, self.password, self.first_name, self.second_name

    def loading_gui(self):
        self.clear_window()
        Label(self.root, text="Loading...").pack()
        self.root.update()

    def item_menu(self, record):
        self.clear_window()

        Label(self.root, text="Item Details", font=("Helvetica", 16)).pack(pady=10)

        Label(self.root, text=f"Name: {record._Record__product_name}").pack()
        Label(self.root, text=f"Code: {record._Record__product_code}").pack()
        Label(self.root, text=f"Quantity: {record._Record__quantity}").pack()
        Label(self.root, text=f"Unit: {record._Record__unit}").pack()

        # --- UPDATE ---
        update_frame = Frame(self.root)
        update_frame.pack(pady=10)

        field_var = StringVar(value="quantity")
        value_var = StringVar()

        OptionMenu(
            update_frame,
            field_var,
            "product_name",
            "quantity",
            "unit"
        ).grid(row=0, column=0, padx=5)

        Entry(update_frame, textvariable=value_var, width=15).grid(row=0, column=1, padx=5)

        def update():
            record.update_record(field_var.get(), value_var.get())
            self.refresh_main_menu()

        Button(update_frame, text="Update", command=update).grid(row=0, column=2, padx=5)

        # --- DELETE ---
        def delete():
            record.delete_record()
            self.refresh_main_menu()

        Button(self.root, text="Delete Item", fg="red", command=delete).pack(pady=5)

        Button(self.root, text="Back", command=self.refresh_main_menu).pack(pady=5)

    def refresh_main_menu(self):
        self.clear_window()
        items = records.Record_manager.read_all(self.user)
        warnings = records.Record_manager.read_low(self.user)
        self.main_menu(warnings, items, self.user)
