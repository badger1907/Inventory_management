import common
import users
import sqlite3
import records
import gui
import users

class Main():
    def __init__(self):
        self.gui = gui.Gui()


    #user authentification stage, must be logged in to acess system
    def user_authentication(self):

            not_loggedin=True
            #keeps going until logged in or program ends
            hastried=False
            username, password, attempt = self.gui.login_gui(hastried)
            while not_loggedin:
                #enters details
                
                if attempt==False:
                    #sign up process
                    self.gui.clear_window()
                    print("---- Sign Up ----")
                    username, password, f_name, s_name = self.gui.signUp_gui()
                    #hashes password
                    e_password  = common.hash_pass(password)
                    #create a user object
                    new_user=users.User(username, e_password)

                    self.gui.clear_window()
                    new_user.sign_up(f_name, s_name)

                else:
                    #hashes password
                    e_password  = common.hash_pass(password)
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
                        hastried=True
                username, password, attempt = self.gui.login_gui(hastried)

            


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

    def menu1(self,user):
        self.gui.main_menu(records.Record_manager.read_low(user),records.Record_manager.read_all(user),user)
        user.logout()



main=Main()
#initial checks
main.start_checks()
#autheticate user
user=main.user_authentication()
still_going=1
while still_going:
    #keep retruning to main menu
    still_going=main.menu1(user)
    
#handle specific erros
#sort sign in with error handling

