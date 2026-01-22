import datetime

class filemanager:

    #adds a new user to the users.txt file
    def new_user(self,f_name,l_name,username,password):
        try:
            file=open("Users.txt","a")
            #username, hashed pass, first name, last name
            Line= f"{username},{str(password)},{f_name},{l_name}\n"
            file.write(Line)
        except:
            print("file handling error occured")
            print(Exception)
        finally:
            file.close()

    #finds a user based of the username they entered, returnung username and password
    #already validated username with find_user
    def get_user(self,username):
        try:
            file=open("Users.txt","r")
            found = False
            #iterates through file
            while found == False:
                line=file.readline()
                line=line.strip()
                file_username, password, f_name, s_name = line.split(',')
                #checks if username is the same as the one on the line
                if file_username == username:
                    found=True
                    file.close()
                    return file_username, password
        except:
            print("file handling error occured")
            file.close()
                
    #checks if there is a user that has the entered username
    def find_user(self, username):
        try:
            file=open("Users.txt","r")
            line = "stuff"
            #iterates through file until empty
            while line != "":
                line=file.readline()
                line=line.strip()
                if line != "":
                    file_username, password, f_name, s_name = line.split(',')
                    #checks if username in file matches enetered username
                    if file_username == username:
                        return True
                    #returns true if exists and false if not
            return False
        except:
            print("file handling error occured")
        finally:
            file.close()

    # enters a log into the log.txt file
    def log(user, action):
        try:
            file = open("log.txt","a")
            file.write(user.username+" did "+action+" on " +datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")
        except:
            print("file handling error occured")
        finally:
            file.close()
            
    # dispalys the contents of the log file line by line
    def view_logs():
        try:
            file = open("log.txt","r")
            line=file.readline()
            while line !="":
                line=file.readline()
                print(line)
        except:
            print("file handling error occured")
        finally:
            file.close()
        



    
# This doesn't work and no one knows why
#     # def get_user(self,username):
#     #     file=open("Users.txt","r")
#     #     found=""
#     #     while username != found:
#     #         line=file.readline()
#     #         list=[]
#     #         cur=""
#     #         print(line)
#     #         for i in range (0,len(line)):
#     #             if line[i] == "," or line[i] == "\n":
#     #                 list.append(cur)
#     #                 cur=""
#     #                 print(", found")
#     #                 print(list)
                    
#     #             else:
#     #                 cur+=line[i]
#     #                 print(cur)
#     #         print(list)
#     #         found=list[0]
#     #     return found
        


#     def find_user(self,username):
#         file=open("Users.txt","r")
#         found=""
#         while username != found:
#             line=file.readline()
#             list=[]
#             cur=""
#             if line != "":
#                 for i in range (0,len(line)):
                    
#                     if line[i] == ",":
#                         list.append(cur)
#                         cur=""
#                         print(list)
#                     else:
#                         cur+=line[i]
#                 found=list[0]
#                 return True
#             else:
#                 return False


    
    