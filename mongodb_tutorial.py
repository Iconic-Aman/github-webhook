import pymongo
from pymongo import MongoClient

def insertDocument():
    studentInfo = {
        "name": "kaus",
        "roll-no": 50,
        "type": "skinny"
    }
    
    student_id = collection.insert_one(studentInfo).inserted_id
    print(f"a new post with id {student_id} has been created ")    
    
def readDocument():
        students_info = collection.find()
        for info in students_info:
            print(info)
        #insert one 
        
def updateDocument():
    collection.update_one({"roll-no": 50}, { '$inc': {"roll-no": 10}})
    
if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    #creating a database
    db = client['skbca-academy']

    #creating a collection
    collection = db.class5
    
    #CRUD -> Create, Read, Update, Delete
    # 1. Create
    #inserting a document
    # insertDocument()
    
    # 2. Read
    #Reading a collection
    readDocument()
    
    # 3. Update
    #updating a document
    # updateDocument()
    
    # 4. Delete
    #Deleting a document
    collection.delete_one({"name": "Himan"})
    
    
    

 