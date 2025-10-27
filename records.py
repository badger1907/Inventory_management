import file_manager
import users
from datetime import datetime
import sqlite3


class Record:
    def __init__(self,product_name,product_code,user,quantity,unit):
        self.__product_name=product_name
        self.__product_code=product_code
        self.__user=user
        self.__quantity=quantity
        self.__unit=unit

        
    def update_record(self, feild, value):
        Record_manager.update(feild,value,self.__user,self.__product_code)
        self.log(self.__user, "updated inventory item "+self.__product_code)

    def write_record(self):
        Record_manager.write(self.__product_name,self.__product_code,self.__user,self.__quantity,self.__unit)
        self.log(self.__user, "added inventory item "+self.__product_code)

    def delete_record(self):
        Record_manager.delete(self.__product_code)
        self.log(self.__user, "deleted inventory item "+self.__product_code)
        #done
    
    def display_record(self):
        print(self.__product_name+","+self.__product_code+","+self.__quantity+","+self.__unit)
        

    def log(self, user, action):
        file = open("log.txt","a")
        file.write(user.username+" did "+action+" on " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")
        file.close()





class Record_manager():

    def read_all(user):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query="""SELECT * FROM Inventory"""
        cursor.execute(query)
        output=cursor.fetchall()
        Connection.commit()
        Connection.close()
        file = open("log.txt","a")
        file.write(user.username+" read inventory at " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")
        file.close()
        return output
    #done ish

    def select(product_code_entered,user):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        valid_code=False    
        while valid_code == False:
            query="""SELECT * FROM Inventory
                    WHERE product_code = '""" + product_code_entered +"'"
            cursor.execute(query)
            item=cursor.fetchone()
            if item != None:
                entry=Record(item[1],item[2],user,item[4],item[5])
                valid_code=True
            else:
                product_code_entered=input("enter a valid product code: ")
        Connection.commit()
        Connection.close()
        return entry

    
    
    def write(product_name,product_code,user,quantity,unit):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query=f"""INSERT INTO Inventory (product_name,product_code,quantity,unit,who,time)
         VALUES (?,?,?,?,?,?)"""
        cursor.execute(query,(product_name,product_code,quantity,unit,user.username,datetime.now()))
        Connection.commit()
        Connection.close()

    def update(feild,value,user,product_code):
        valid_feilds=["product_name","Product_code","quantity","unit"]
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        valid=False
        while valid==False:
            for i in range (0,len(valid_feilds)):
                if valid_feilds[i] == feild:
                    valid=True
            if valid==False:
                print("invalid - feild name not valid")
                feild=input("enter the feild (product_name,Product_code,quantity,unit) you would like to change: ")
                value=input("enter the value you would like to change it to: ")
                
        query="UPDATE Inventory SET '"+feild+"' = ? WHERE product_code = ?"
        query2="""UPDATE Inventory SET who = ? WHERE product_code = ?"""  
        cursor.execute(query,(value,product_code))
        cursor.execute(query2,(user.username,product_code))
        Connection.commit()
        Connection.close()

    def delete(product):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query="""DELETE FROM Inventory WHERE
                Product_code = '"""+product+"'"
        cursor.execute(query)
        Connection.commit()
        Connection.close()


