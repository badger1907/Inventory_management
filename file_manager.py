import datetime

class filemanager:

    def new_user(self,f_name,l_name,username,password):
        file=open("Users.txt","a")
        #username, hashed pass, first name, last name
        Line= f"{username},{str(password)},{f_name},{l_name}\n"
        file.write(Line)
        file.close()

    def get_user(self,username):
        file=open("Users.txt","r")
        found = False
        while found == False:
            line=file.readline()
            line=line.strip()
            file_username, password, f_name, s_name = line.split(',')
            if file_username == username:
                found=True
                file.close()
                return file_username, password
                
    
    def find_user(self,username):
        file=open("Users.txt","r")
        line = "stuff"
        while line != "":
            line=file.readline()
            line=line.strip()
            if line != "":
                file_username, password, f_name, s_name = line.split(',')
                if file_username == username:
                    return True
        return False
    
    def log(user, action):
        file = open("log.txt","a")
        file.write(user.username+" did "+action+" on " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")
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


    
    