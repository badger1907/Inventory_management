from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import common
import records
import users

class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("750x500")
        self.user=None
        self.current_items = []

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



    def main_menu(self, warning_items, items,user):
        self.user=user
        self.clear_window()

        Label(self.root, text="Inventory", font=("Helvetica", 16)).pack(pady=10)

            # search control
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

        def search():
            feild = field_var.get()
            value = value_var.get()

            results = records.Record_manager.search(feild, value, user)

        Button(
            search_frame,
            text="Search",
            command=search
        ).grid(row=0, column=2, padx=5)

        Label(self.root, text="All Items").pack(pady=5)



        # tree table
        table_frame = Frame(self.root)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "code", "qty", "unit"),
            show="headings",
            height=15
        )

        self.tree.heading("name", text="Product Name")
        self.tree.heading("code", text="Code")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("unit", text="Unit")

        self.tree.column("name", width=260)
        self.tree.column("code", width=120)
        self.tree.column("qty", width=80, anchor=CENTER)
        self.tree.column("unit", width=80, anchor=CENTER)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)


        combined_items = []
        if warning_items:
            combined_items.extend(warning_items)
        combined_items.extend(items)



        self.populate_tree(combined_items, warning_items)


        def open_selected(event=None):
            selected = self.tree.selection()
            if not selected:
                return

            index = self.tree.index(selected[0])
            record = self.current_items[index]
            self.item_menu(record)

        self.tree.bind("<Double-1>", open_selected)

       

        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        Button(
            button_frame,
            text="Create New Item",
            width=18,
            fg="green",
            command=self.create_item_menu
        ).pack(side=LEFT, padx=5)

        Button(
            button_frame,
            text="Admin Login",
            width=18,
            fg="blue",
            command=self.admin_login_gui
        ).pack(side=LEFT, padx=5)

        self.root.mainloop()

    def populate_tree(self, items, warning_items):
        self.tree.delete(*self.tree.get_children())
        self.current_items = items

        for item in items:
            tag = "low" if item in warning_items else "normal"

            self.tree.insert(
                "",
                END,
                values=(
                    item._Record__product_name,
                    item._Record__product_code,
                    item._Record__quantity,
                    item._Record__unit
                ),
                tags=(tag,)
            )

        self.tree.tag_configure("low", foreground="red")

    def admin_login_gui(self):
        self.clear_window()

        Label(self.root, text="Admin Login", font=("Helvetica", 16)).pack(pady=10)

        Label(self.root, text="Admin Password").pack()
        password_entry = Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def login():
            admin_password = password_entry.get()
            admin_user=users.User("admin", common.hash_pass(admin_password))
            found=admin_user.admin_login(admin_user)

            if found:
                self.admin_menu()
            else:
                messagebox.showerror("Error", "Incorrect admin password")

        Button(self.root, text="Login", command=login).pack(pady=5)
        Button(self.root, text="Back", command=self.refresh_main_menu).pack(pady=5)

    def admin_menu(self):
        self.clear_window()

        Label(self.root, text="Admin Area", font=("Helvetica", 16)).pack(pady=10)

        Button(
            self.root,
            text="View Logs",
            width=20,
            command=self.view_logs_gui
        ).pack(pady=5)

        Button(
            self.root,
            text="Back to Inventory",
            width=20,
            command=self.refresh_main_menu
        ).pack(pady=10)

    def view_logs_gui(self):
        self.clear_window()

        Label(self.root, text="System Logs", font=("Helvetica", 16)).pack(pady=10)

        text = Text(self.root, width=80, height=20)
        text.pack(padx=10, pady=5)

        try:
            with open("log.txt", "r") as file:
                text.insert(END, file.read())
        except FileNotFoundError:
            text.insert(END, "No logs found.")

        text.config(state=DISABLED)

        Button(
            self.root,
            text="Back",
            command=self.admin_menu
        ).pack(pady=5)




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
        #Display the login screen and return (username, password, attempt=True)
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
            self.root.quit()     # exit mainloop

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
