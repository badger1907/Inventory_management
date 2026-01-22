import file_manager

class User:
    def __init__(self,username,password):

        self.password=password
        self.username=username
        self.logged_in = False

    def display(self):
        return str(self.username)

    #checks if user logged in
    def is_logged_in(self):
        return self.logged_in
    
    #allows user to create an account
    def sign_up(self,f_name,s_name):
        try:
            #displays menu
            print ("--- sign up ---")
            system = file_manager.filemanager()
            #checks username not alreasy in use
            while system.find_user(self.username):
                self.username=input("enter a diffent username")
            #adds a new user
            system.new_user(f_name,s_name,self.username,self.password)
            status=""
        except:
            print("sign up failed")
            status="failed"
        finally:
            #logs actions
            file_manager.filemanager.log(self,status+"signed up")
    
    #allows a user to login
    def login(self):
        try:
            system = file_manager.filemanager()
            #checks username exists
            if system.find_user(self.username):
                #gets user from file
                username, password = system.get_user(self.username)
                if password==self.password:
                    #sets login to be true
                    self.logged_in = True
                    print("login succesful")
                    #logs actions
                    file_manager.filemanager.log(self,"logged in")
                    return 1
                else:
                    print("password incorrect - try again")
                return 2
            else:
                #account not found - explained in main
                return 0
        except:
            print("login failed")
    
    #admin login system
    def admin_login(self,user):
        try:
            #password stored in secure file
            file=open("admins.txt","r")
            password=file.readline()
            #checks password and logs outcome
            if self.password==password:
                file_manager.filemanager.log(user,"logged in as an admin")
                return True
            else:
                file_manager.filemanager.log(user,"FAILED(password incorrect) at logging in as an admin")
                return False
        except:
            print("admin login failed")
            
    def logout(self):
        self.logged_in=False
        file_manager.filemanager.log(self,"logged out")

    def find_user(username):
        system = file_manager.filemanager()
        return system.find_user(username)

