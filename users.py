import file_manager

class User:
    def __init__(self,username,password):

        self.password=password
        self.username=username
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in
    
    def sign_up(self):
        try:
            print ("--- sign up ---")
            system = file_manager.filemanager()
            f_name=input("enter your first name: ")
            s_name=input("enter your second name: ")
            while system.find_user(self.username):
                self.username=input("enter a diffent username")
            system.new_user(f_name,s_name,self.username,self.password)
            status=""
        except:
            print("sign up failed")
            status="failed"
        finally:
            file_manager.filemanager.log(self,status+"signed up")
    
    def login(self):
        try:
            system = file_manager.filemanager()
            if system.find_user(self.username):
                username, password = system.get_user(self.username)
                #print("file username:"+username)
                #print("file password:"+password)
                if password==self.password:
                    self.logged_in = True
                    print("login succesful")
                    file_manager.filemanager.log(self,"logged in")
                    return 1
                else:
                    print("password incorrect - try again")
                return 2
            else:
                return 0
        except:
            print("login failed")
    
    def admin_login(self,user):
        try:
            file=open("admins.txt","r")
            password=file.readline()
            if self.password==password:
                file_manager.filemanager.log(user,"logged in as an admin")
                return True
            else:
                file_manager.filemanager.log(user,"FAILED(password incorrect) at logging in as an admin")
                return False
        except:
            print("admin login failed")
        


# 0 - account not found
# 1 - login sucesful
# 2 - login failed