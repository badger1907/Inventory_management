from file_manager import filemanager
from record_manager import Record_manager

#record class, deals with users data and changes
class Record:
    def __init__(self,product_name,product_code,user,quantity,unit):
        self.__product_name=product_name
        self.__product_code=product_code
        self.__user=user
        self.__quantity=quantity
        self.__unit=unit

    #updates record and logs change
    def update_record(self, feild, value):
        try:
            Record_manager.update(feild,value,self.__user,self.__product_code)
            status=""
            
        except:
            print("error occured trying to update record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"updated inventory item "+self.__product_code)

    #writes record and logs chnage
    def write_record(self):
        try:
            Record_manager.write(self.__product_name,self.__product_code,self.__user,self.__quantity,self.__unit)
            status=""
        except:
            print("error occured trying to create a record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"added inventory item "+self.__product_code)


    #deletes record and logs chnage
    def delete_record(self):
        try:
            Record_manager.delete(self.__product_code)
            status=""
        except:
            print("error occured trying to delete a record")
            status="failed"
        finally:
            filemanager.log(self.__user, status+"deleted inventory item "+self.__product_code)

    #displays record    
    def display_record(self):
        try:
            print(self.__product_name+","+self.__product_code+","+self.__quantity+","+self.__unit)
        except:
            print("error occured trying to display a record")
        

    






