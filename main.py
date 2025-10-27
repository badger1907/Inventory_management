import users
import hashlib
import sqlite3
import records
import datetime

def user_authentication():
    not_loggedin=True
    while not_loggedin:
        print("******************************")
        print(" -- Login --")
        username=input("enter yout username: ")
        password=input("enter your password: ")
        print("-----------")
        password=str.encode(password)
        sha256=hashlib.sha256()
        sha256.update(password)
        e_password  = sha256.hexdigest()
        unconfirmed_user=users.User(username, e_password)
        found=unconfirmed_user.login()
        if found == 1:
            not_loggedin=False
            print("******************************")
            return unconfirmed_user
        elif found == 2:
            print("")
        else:
            print("we couldnt find your acount")
            option=int(input("enter 1 for sign up or 2 for quit"))
            if option == 1:
                unconfirmed_user.sign_up()
                print ("sign up complete")
            else:
                not_loggedin=False
        print("******************************")
        print("error - please try again later")


def start_checks():
    #check file exists

        
        
    #check adtabse exists
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
    connection.close()

def menu1(user):
    inp=""
    print("welcome to Fylde Aero Inventory system")
    print("This is currently being run in the command line")
    valid=False
    while valid==False:
        print("if you would like to see what is in the databse, press 1")
        print("if you would like to create an entry, press 2")
        print("Please enter '/' to exit")
        inp=input("Enter a value (1,2 or '/'): ")
        if inp == "1":
            print("items displayed")
            array_records=records.Record_manager.read_all(user)
            for item in array_records:
                print(item)
            valid=True
            menu2(user)
        elif inp == "2":
            checked=False
            while checked==False:
                checked=True
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
            record=records.Record(record_name,record_code,user,quantity,unit)
            record.write_record()
            valid=True
        elif inp=="/":
            print("you have exited the application")
            valid=True
            return False
        else:
            print("not a valid input, try again")
    return True

def menu2(user):
    print("please select an entry to work with")
    code=input("enter the product-code of the entry: ")   
    entry=records.Record_manager.select(code,user)
    #validation inside read
    print("you have selected:")
    entry.display_record()
    valid=False
    while valid==False:
        print("1 - update record")
        print("2 - delete record")
        print("/ - to escape")
        inp=input("What would you like to do with the selected record: ")
        match inp:
            case "1":
                feild=input("enter the feild (product_name,Product_code,quantity,unit) you would like to change: ")
                value=input("enter the value you would like to change it to: ")
                entry.update_record(feild,value)
                #validation inside update
                valid=True
            case "2":
                entry.delete_record()
                valid=True
            case "/":
                valid=True
            case _:
                print("invalid option - try again")
    menu1(user)

#initial checks
start_checks()
#autheticate user
user=user_authentication()
#use databse
still_going=1
while still_going:
    still_going=menu1(user)
    


