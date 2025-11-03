import users
import hashlib
import sqlite3
import records
import file_manager

class main():

    #user authentification stage, must be logged in to acess system
    def user_authentication(self):
        try:
            not_loggedin=True
            #keeps going until logged in or program ends
            while not_loggedin:
                #enters details
                print("*****************************************")
                print(" -- Login --")
                username=input("enter yout username: ")
                password=input("enter your password: ")
                print("-----------")
                #hashes password
                password=str.encode(password)
                sha256=hashlib.sha256()
                sha256.update(password)
                e_password  = sha256.hexdigest()
                #create a user object
                unconfirmed_user=users.User(username, e_password)
                found=unconfirmed_user.login()
                # based of outcome of login
                if found == 1:
                    #logged in sucesfully
                    not_loggedin=False
                    print("*****************************************")
                    return unconfirmed_user
                elif found == 2:
                    #login failed, allows user to try again
                    print("")
                else:
                    #no account found
                    print("we couldnt find your acount")
                    option=int(input("enter 1 for sign up, 2 to try again or 3 to quit"))
                    if option == 1:
                        #user signs up then tries to login again
                        unconfirmed_user.sign_up()
                        print ("sign up complete")
                    elif option == 3:
                        #exits program
                        not_loggedin=False
                        exit(1)
                    #2 or anything else will let the user try again
        except:
            print("everything broke again")


    def start_checks(self):  
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
        try:
            inp=""
            #welcome lines
            print("*****************************************")
            print("welcome to Fylde Aero Inventory system")
            print("This is currently being run in the command line")
            print("---------------------------------")
            valid=False
            #options with validation
            while valid==False:
                print("1 - See table")
                print("2 - create an entry")
                print("3 - search")
                print("4 - admin mode")
                print("/ - exit")
                inp=input("Enter a value (1-4 or '/'): ")
                print("---------------------------------")
                if inp == "1":
                    #displays table
                    print("")
                    print("---Inventory---")
                    #reads all theitems into an array and displays line by line
                    array_records=records.Record_manager.read_all(user)
                    for item in array_records:
                        print(item)
                    valid=True
                    print("--------------")
                    self.menu2(user)
                elif inp == "2":
                    #creates a new record
                    checked=False
                    #validation and data entry
                    while checked==False:
                        checked=True
                        print("")
                        print("---Create entry---")
                        record_name=input("enter the name of the item: ")
                        record_code=input("enter the product code: ")
                        quantity=input("enter the quantity: ")
                        if quantity.isdigit() == True:
                            if int(quantity)<0:
                                checked=False
                                print("error - must be greater than 0")
                                continue
                        else:
                            checked=False
                            print("error - must be a number")
                            continue
                        unit=input("enter the unit: ")
                        print("------")
                    #creates record and writes it to the database    
                    record=records.Record(record_name,record_code,user,quantity,unit)
                    record.write_record()
                    valid=True
                elif inp == "3":
                    #search the table
                    print("")
                    print("---search---")
                    feild=input("enter the feild (product_name,Product_code,quantity,unit,who) you are searching: ")
                    value=input("enter the value you are searching: ")
                    #entered values then searched (validation in function)
                    records.Record_manager.search(feild,value,user)
                    valid=True
                    #option to select a entry or go back to the main menu
                    print("--------------")
                    entry=input("select field(s) yes/no: ")
                    if input== "yes":
                        self.menu2(user)
                    else:
                        self.menu1(user)
                elif inp=="/":
                    #exits application
                    print("you have exited the application")
                    user.logout()
                    exit(1)
                elif inp == "4":
                    #admin mode
                    self.admin(user)
                else:
                    print("not a valid input, try again")
            return True
        except:
            user.logout()

    #second meu allowing the user to select a single record
    def menu2(self,user):
        try:
            #menu page
            print(" ")
            print("please select an entry to work with")
            code=input("enter the product-code of the entry: ")   
            entry=records.Record_manager.select(code,user)
            #validation inside read
            print("you have selected:")
            entry.display_record()
            valid=False
            print("---------------------")
            #options availible
            while valid==False:
                print("1 - update record")
                print("2 - delete record")
                print("/ - to escape")
                inp=input("What would you like to do with the selected record: ")
                match inp:
                    case "1":
                        #update record
                        feild=input("enter the feild (product_name,Product_code,quantity,unit) you would like to change: ")
                        value=input("enter the value you would like to change it to: ")
                        entry.update_record(feild,value)
                        #validation inside update
                        valid=True
                    case "2":
                        #delete record
                        entry.delete_record()
                        valid=True
                    case "/":
                        #exit
                        valid=True
                    case _:
                        print("invalid option - try again")
            self.menu1(user)
        except:
            print("broken")
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

main=main()
#initial checks
main.start_checks()
#autheticate user
user=main.user_authentication()
still_going=1
while still_going:
    #keep retruning to main menu
    still_going=main.menu1(user)
    


