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
        self.__time=datetime.now()
        
    def update_record(self, feild, value):
        #set up quesry changing specific feild
        query="""UPDATE Inventory SET {0} = {1} WHERE product_code = {2}""",feild,value,self.__product_code
        record_manager= Record_manager()
        record_manager.Update(query,self.__user,self.__product_code)
        self.log(self.__user, "updated inventory item "+self.__product_code)
        #done  

    def write_record(self):
        record_manager= Record_manager()
        record_manager.write(self.__product_name,self.__product_code,self.__user,self.__quantity,self.__unit)
        self.log(self.__user, "added inventory item "+self.__product_code)

    def delete_record(self):
        record_manager= Record_manager()
        record_manager.Delete(self.__product_code)
        self.log(self.__user, "deleted inventory item "+self.__product_code)
        #done
    
    def read_record(self,product_code):
        record_manager=Record_manager()
        item=record_manager.read(product_code)
        self.log(self.__user, "read inventory item "+self.__product_code)
        print(item)
        

    def log(self, user, action):
        file = open("log.txt","a")
        file.write(f"{0} did {1} on {2}",user.username, action, datetime.now())
        file.close()



class Record_manager():
    def __init__(self):
        sqliteConnection = sqlite3.connect('inventory.db')
        global cursor
        cursor = sqliteConnection.cursor()
        #done

    def read_all():
        query="""SELECT * FROM Inventory"""
        cursor.execute(query)
        output=cursor.fetchall()
        array=[]
        for row in output:
            record=Record(row)
            array.append(record)
        cursor.commit()
        return array
    #done ish

    def read(product_code):
        query="""SELECT * FROM Inventory
                WHERE product_code = {0}""",product_code
        item = cursor.execute(query)
        cursor.commit()
        return item
    #done
    
    def write(product_name,product_code,user,quantity,unit):
        query=f"""INSERT INTO Inventory (product_name,product_code,quantity,unit,who,time)
                VALUES ({0},{1},{2},{3},{4},{5})""",product_name,product_code,user,quantity,unit
        cursor.execute(query)
        cursor.commit()
        #done

    def update(query,user,product_code):
        query2="""UPDATE Inventory SET user = {1} WHERE product_code = {2}""",user.username,product_code   
        cursor.execute(query)
        cursor.execute(query2)
        cursor.commit()
        #done

    def delete(product):
        query="""DELETE FROM Inventory WHERE
                product_code = '"""+product+"'"
        cursor.execute(query)
        cursor.commit()
        #done