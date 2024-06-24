import numpy as np
import pickle 
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
# MongoDB connection details
atlas_url = 'mongodb+srv://sathvikt23a:rKRC5yAGpbiSvhuD@cluster0.8dtd3nj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(atlas_url)
dataaa=[]
client = MongoClient(atlas_url)
database = client['CentralData']
collection= database['UserData']

        # Query for a movie that has the title 'Back to the Future'
        

