from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import numpy as np
import pickle 
# MongoDB connection details
atlas_url = 'con string '
client = MongoClient(atlas_url)
database = client["CentralData"]
collection= database['embeddings']





# Connect to the MongoDB server
"""
# Access the database and collections
db = client['CentralData']
userdata1_collection = db['UserData']
embeddings1_collection = db['embeddings']
username="Sathvik"
# Define the aggregation pipeline
pipeline = [
    {
        '$match': {'username': f'{username}'}
    },
    {
        '$lookup': {
            'from': 'embeddings',
            'localField': 'data',
            'foreignField': 'data',
            'as': 'embedding'
        }
    },
    {
        '$unwind': '$embedding'
    }
]

# Execute the aggregation query
results = userdata1_collection.aggregate(pipeline)
final=[]
# Process the results
for result in results:
    final.extend(result["embedding"]["embedding"])
print(final)"""
class access:
    def UpdateEmbedding(dataName,data):
         db = client['CentralData']
         embeddings1_collection = db['embeddings']
         final={
                "data":dataName,
                "embedding":pickle.dumps(data)
            }
         embeddings1_collection.insert_one(final)
         print("Data uploaded ")
    def UpdateUserData(dataname , username):
         db = client['CentralData']
         embeddings1_collection = db['UserData']
         final={
                "username":username,
                "data":dataname
            }
         embeddings1_collection.insert_one(final)
         print("Data uploaded ")
    def CheckDataName(database , coll , dataname ):
         db = client[database]
         collection = db[coll]
         info=collection.find({"data":dataname})
         #print(len(list(info)))
         if len(list(info))==0:
              print("Not present ")
              return 1
         else:
              
              print("present")
              return 0
    def CheckUserData(username , dataname  ):
         db = client["CentralData"]
         collection = db["UserData"]
         info=collection.find({"username":username ,"data":dataname})
         
         #print(len(list(info)))
         for i in info :
             if i["data"]==dataname:
                print("Present ")
                return 0
         print(" Not present")
         return 1
        
    def UpdatePages_and_texts(dataname ,pages_and_texts):
         db = client['CentralData']
         collection = db['PagesAndTexts']
         final={
                "data":dataname,
                "pages_and_texts":pages_and_texts
            }
         collection.insert_one(final)
    
         
    def GetAllUserEmbeddings(username):
        db = client['CentralData']
        userdata1_collection = db['UserData']
        embeddings1_collection = db['embeddings']
        pipeline = [
                {
                    '$match': {'username': f'{username}'}
                },
                {
                    '$lookup': {
                        'from': 'embeddings',
                        'localField': 'data',
                        'foreignField': 'data',
                        'as': 'embedding'
                    }
                },
                {
                    '$unwind': '$embedding'
                }
            ]

            # Execute the aggregation query
        results = userdata1_collection.aggregate(pipeline)
        final=[]
            # Process the results
        for result in results:
                final.extend(pickle.loads(result["embedding"]["embedding"]))
        return final
#access.CheckUserData('Hari' ,"foods")

