from tkinter import *

class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("400x200")

        # These will store the input values
        self.username = None
        self.password = None
        self.attempt = None

    def clear_window(self):
        """Remove all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_gui(self):
        """Display the login screen and return (username, password, attempt=True)."""
        self.clear_window()

        Label(self.root, text="Login").grid(row=0, column=0, columnspan=2, pady=5)

        Label(self.root, text="Username:").grid(row=1, column=0, sticky=E)
        username_entry = Entry(self.root)
        username_entry.grid(row=1, column=1, pady=5)

        Label(self.root, text="Password:").grid(row=2, column=0, sticky=E)
        password_entry = Entry(self.root, show="*")
        password_entry.grid(row=2, column=1, pady=5)

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
        first_name=""
        second_name=""

        def signup():
            self.username = username_entry.get()
            self.password = password_entry.get()
            first_name = first_name_entry.get()
            second_name = second_name_entry.get()
            self.root.quit()  # exit mainloop

        Button(self.root, text="Sign Up", command=signup, width=15).grid(row=5, column=0, columnspan=2, pady=10)
        self.root.mainloop()

        return self.username, self.password, first_name, second_name
    
    def loading_gui(self):
        self.clear_window()
        Label(self.root, text="Loading...").pack()
        self.root.update()