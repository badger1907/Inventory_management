import sqlite3
from file_manager import filemanager
from datetime import datetime
from records import Record

# interacts with the database
class Record_manager():

    #gets all records in the database and places them in an array
    def read_all(user):
        try:
            #access invenotry and runs query
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
            #logs change and closes file     
            file.write(user.username+" read "+status+" inventory at " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")      
            Connection.close()
            file.close()
        return output
    
    #creates a record object based of a selected rerod from the database
    def select(product_code_entered,user):
        try:
             #access invenotry and runs query
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            valid_code=False    
            #checks its a valid product code
            while valid_code == False:
                query="""SELECT * FROM Inventory
                        WHERE product_code = '""" + product_code_entered +"'"
                cursor.execute(query)
                item=cursor.fetchone()
                #if item exists create object
                if item != None:
                    entry=Record(item[1],item[2],user,item[4],item[5])
                    valid_code=True
                else:
                    product_code_entered=input("enter a valid product code: ")
        except:
            print("error occured - select failed")
        finally:
            #close all and log
            Connection.commit()
            Connection.close()
            filemanager.log(user,"selected"+product_code_entered)
        return entry

    #search table based of feild and value
    def search(feild,value,user):
        try:
            #access invenotry and runs query
            valid_feilds=["product_name","Product_code","quantity","unit","who"]
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            valid=False
            #checks valid field
            while valid==False:
                for i in range (0,len(valid_feilds)):
                    if valid_feilds[i] == feild:
                        valid=True
                if valid==False:
                    print("invalid - feild name not valid")
                    feild=input("enter the feild (product_name,Product_code,quantity,unit,) you would to search through: ")
                    value=input("enter the value you would like to search: ")
            query="""SELECT * FROM Inventory
                    WHERE """+feild+ "= '"+value+"';"
            cursor.execute(query)
            rows=cursor.fetchall()
            #displays records found
            for row in rows:
                print(row)
        except:
            print("error occured - search failed")
        finally:
            #close and log
            filemanager.log(user,"searched in "+feild+ " value")
            Connection.commit()
            Connection.close()
                
        

    #writes data into the table
    def write(product_name,product_code,user,quantity,unit):
        try:
            #access invenotry and runs query
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            query=f"""INSERT INTO Inventory (product_name,product_code,quantity,unit,who,time)
            VALUES (?,?,?,?,?,?)"""
            cursor.execute(query,(product_name,product_code,quantity,unit,user.username,datetime.now()))
        except:
            print("error occured - write failed")
        finally:
            #close
            Connection.commit()
            Connection.close()
   
    #update a record in the table
    def update(feild,value,user,product_code):
        try:
            #access invenotry and runs query
            valid_feilds=["product_name","Product_code","quantity","unit"]
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            valid=False
            #checks valid field
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
            #close all
            Connection.commit()
            Connection.close()
   
    #deltes record from table
    def delete(product):
        try:
            #access invenotry and runs query
            Connection = sqlite3.connect('inventory.db')
            cursor = Connection.cursor()
            query="""DELETE FROM Inventory WHERE
                    Product_code = '"""+product+"'"
            cursor.execute(query)
        except:
            print("error occured - delete failed")
        finally:
            #close all
            Connection.commit()
            Connection.close()
