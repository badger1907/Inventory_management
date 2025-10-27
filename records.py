from file_manager import filemanager
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
        try:
            Record_manager.update(feild,value,self.__user,self.__product_code)
            status=""
            
        except:
            print("error occured trying to update record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"updated inventory item "+self.__product_code)

    def write_record(self):
        try:
            Record_manager.write(self.__product_name,self.__product_code,self.__user,self.__quantity,self.__unit)
            status=""
        except:
            print("error occured trying to create a record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"added inventory item "+self.__product_code)

    def delete_record(self):
        try:
            Record_manager.delete(self.__product_code)
            status=""
        except:
            print("error occured trying to delete a record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"deleted inventory item "+self.__product_code)
    
    def display_record(self):
        try:
            print(self.__product_name+","+self.__product_code+","+self.__quantity+","+self.__unit)
        except:
            print("error occured trying to display a record")
        

    





class Record_manager():

    def read_all(user):
        try:
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            query="""SELECT * FROM Inventory"""
            cursor.execute(query)
            output=cursor.fetchall()
            file = open("log.txt","a")
            Connection.commit()
            status=""
        except:
            print("error occured - display failed")
            status="failed"       
        finally:     
            file.write(user.username+" read "+status+" inventory at " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")      
            Connection.close()
            file.close()
        return output
    

    def select(product_code_entered,user):
        try:
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
        except:
            print("error occured - select failed")
        finally:
            Connection.commit()
            Connection.close()
            filemanager.log(user,"selected"+product_code_entered)
        return entry

    def search(feild,value):
        try:
            valid_feilds=["product_name","Product_code","quantity","unit","who"]
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            valid=False
            while valid==False:
                for i in range (0,len(valid_feilds)):
                    if valid_feilds[i] == feild:
                        valid=True
                if valid==False:
                    print("invalid - feild name not valid")
                    feild=input("enter the feild (product_name,Product_code,quantity,unit,who) you are searching: ")
                    value=input("enter the value you are searching: ")
            query="""SELECT * FROM Inventory
                    WHERE """+feild+ "= '"+value+"'"
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows:
                print(row)
        except:
            print("error occured - search failed")
        finally:
            Connection.commit()
            Connection.close()
                
        


    def write(product_name,product_code,user,quantity,unit):
        try:
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            query=f"""INSERT INTO Inventory (product_name,product_code,quantity,unit,who,time)
            VALUES (?,?,?,?,?,?)"""
            cursor.execute(query,(product_name,product_code,quantity,unit,user.username,datetime.now()))
        except:
            print("error occured - write failed")
        finally:
            Connection.commit()
            Connection.close()

    def update(feild,value,user,product_code):
        try:
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
        except:
            print("error occured - update failed")
        finally:
            Connection.commit()
            Connection.close()

    def delete(product):
        try:
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            query="""DELETE FROM Inventory WHERE
                    Product_code = '"""+product+"'"
            cursor.execute(query)
        except:
            print("error occured - delete failed")
        finally:
            Connection.commit()
            Connection.close()


