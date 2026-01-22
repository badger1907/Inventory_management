import users
import hashlib
import sqlite3
import records
import file_manager
import gui
import users

class Main():
    def __init__(self):
        self.gui = gui.Gui()


    def hash_pass(password):
        password=str.encode(password)
        sha256=hashlib.sha256()
        sha256.update(password)
        e_password  = sha256.hexdigest()
        return e_password

    #user authentification stage, must be logged in to acess system
    def user_authentication(self):

            not_loggedin=True
            #keeps going until logged in or program ends
            username, password, attempt = self.gui.login_gui(False)
            while not_loggedin:
                #enters details
                
                if attempt==False:
                    #sign up process
                    self.gui.clear_window()
                    print("---- Sign Up ----")
                    username, password, f_name, s_name = self.gui.signUp_gui()
                    #hashes password
                    e_password  = Main.hash_pass(password)
                    #create a user object
                    new_user=users.User(username, e_password)

                    self.gui.clear_window()
                    new_user.sign_up(f_name, s_name)
                else:
                    #hashes password
                    e_password  = Main.hash_pass(password)
                    #create a user object
                    unconfirmed_user=users.User(username, e_password)
                    found=unconfirmed_user.login()
                    # based of outcome of login
                    if found == 1:
                        #logged in sucesfully
                        not_loggedin=False
                        self.gui.clear_window()
                        self.gui.setUser(unconfirmed_user)
                        return unconfirmed_user
                    else:
                        self.gui.clear_window()
                username, password, attempt = self.gui.login_gui(True)

            


    def start_checks(self):  
        self.gui.loading_gui()
        try:
            file=open("users.txt","x")
            print("file made")
        except:
            print("file aleady exists")
        #check databse and table exists
        try:
            connection=sqlite3.connect("inventory.db")
            cursor = connection.cursor()
            table_creation="""CREATE TABLE IF NOT EXISTS Inventory(
                    id INTEGER PRIMARY KEY,
                    product_name VARCHAR(25),
                    Product_code VARCHAR(25),
                    quantity INTEGER,
                    unit VARCHAR(5),
                    who VARCHAR(25),
                    time VARCHAR(25));
            """
            cursor.execute(table_creation)
            connection.commit()
        except:
                print("databse error")
        finally:
            connection.close()


    #first meu seen by user
    #display table, create an entry, search the table, enter admin mode or quit
    def menu1(self,user):
        self.gui.main_menu(records.Record_manager.read_low(user),records.Record_manager.read_all(user),user)
        user.logout()

#admin menu
    def admin(self,user):
        try:
            #login menu
            print(" -- Login --")
            password=input("enter your password: ")
            print("-----------")
            #hasing password
            password=str.encode(password)
            sha256=hashlib.sha256()
            sha256.update(password)
            e_password  = sha256.hexdigest()
            #create a 
            admin_user=users.User("admin", e_password)
            found=admin_user.admin_login(user)
            if found:
                #options once logged in
                print("login sucesful")
                print("1 - view logs")
                print("2 - return to main menu")
                inp=input()
                if inp=="1":
                    file_manager.filemanager.view_logs()
            else:
                #login failed messages
                print("login failed")
                print("your atempts has been logged")
            self.menu1(user)
        except:
            print("no admins today")

main=Main()
#initial checks
main.start_checks()
#autheticate user
user=main.user_authentication()
still_going=1
while still_going:
    #keep retruning to main menu
    still_going=main.menu1(user)
    


