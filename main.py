import users
import hashlib

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
        #print("entered username:"+username)
        #print("enteered hashed pass:"+e_password)
        unconfirmed_user=users.User(username, e_password)
        found=unconfirmed_user.login()
        print(found)
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
    pass


start_checks()
user_authentication()
