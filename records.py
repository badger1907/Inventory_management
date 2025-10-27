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
        #set up quesry changing specific feild
        query="""UPDATE Inventory SET {0} = {1} WHERE product_code = {2}""",feild,value,self.__product_code
        Record_manager.Update(query,self.__user,self.__product_code)
        self.log(self.__user, "updated inventory item "+self.__product_code)
        #done  

    def write_record(self):
        Record_manager.write(self.__product_name,self.__product_code,self.__user,self.__quantity,self.__unit)
        self.log(self.__user, "added inventory item "+self.__product_code)

    def delete_record(self):
        Record_manager.Delete(self.__product_code)
        self.log(self.__user, "deleted inventory item "+self.__product_code)
        #done
    
    def read_record(self,product_code):
        item=Record_manager.read(product_code)
        self.log(self.__user, "read inventory item "+self.__product_code)
        print(item)
        

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
        array=[]
        # for row in output:
        #     record=Record(row[1],)
        #     array.append(record)
        Connection.commit()
        Connection.close()
        file = open("log.txt","a")
        file.write(user.username+" read inventory at " +datetime.now().strftime("%d/%m/%y, %H:%M:%S")+"\n")
        file.close()
        return output
    #done ish

    def read(product_code):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query="""SELECT * FROM Inventory
                WHERE product_code = {0}""",product_code
        item = cursor.execute(query)
        Connection.commit()
        Connection.close()
        return item
    #done
    
    def write(product_name,product_code,user,quantity,unit):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query=f"""INSERT INTO Inventory (product_name,product_code,quantity,unit,who,time)
         VALUES (?,?,?,?,?,?)"""
        cursor.execute(query,(product_name,product_code,quantity,unit,user.username,datetime.now()))
        Connection.commit()
        Connection.close()

    def update(query,user,product_code):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query2="""UPDATE Inventory SET user = {1} WHERE product_code = {2}""",user.username,product_code   
        cursor.execute(query)
        cursor.execute(query2)
        Connection.commit()
        Connection.close()
        #done

    def delete(product):
        Connection = sqlite3.connect('inventory.db')
        cursor = Connection.cursor()
        query="""DELETE FROM Inventory WHERE
                product_code = '"""+product+"'"
        cursor.execute(query)
        Connection.commit()
        Connection.close()
        #done

