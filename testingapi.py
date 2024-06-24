from pymongo import MongoClient

from pymongo.errors import ConnectionFailure, OperationFailure
import pickle
# MongoDB connection details
atlas_url = 'mongodb+srv://sathvikt23a:rKRC5yAGpbiSvhuD@cluster0.8dtd3nj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
dbName = "sample_mflix"
data=[{'page_number': -39, 'sentence_chunk': 'Human Nutrition: 2020 Edition UNIVERSITY OF HAWAI‘I ATMĀNOA FOOD SCIENCE AND HUMAN NUTRITION PROGRAM ALAN TITCHENAL, SKYLAR HARA, NOEMI ARCEO CAACBAY, WILLIAMMEINKE-LAU, YA-YUN YANG, MARIE KAINOA FIALKOWSKI REVILLA, JENNIFER DRAPER, GEMADY LANGFELDER, CHERYL GIBBY, CHYNA NICOLE CHUN, AND ALLISON CALABRESE', 'chunk_char_count': 308, 'chunk_word_count': 42, 'chunk_token_count': 77.0, 'embedding': ([ 6.74242824e-02,  9.02280957e-02, -5.09550422e-03, -3.17545682e-02,7.39082173e-02,  3.51976342e-02, -1.97986923e-02,  4.67692427e-02])}]
final={
     "name":"health",
     "data":data
}
try:
    # Connect to MongoDB
        client = MongoClient(atlas_url)
        database = client['CentralData']
        collection= database['UserData']

        # Query for a movie that has the title 'Back to the Future'
        query = {'title': 'Back to the Future'}
        data=collection.find({"username":"Sathvik"})
        j=0
        
        for i in data :
             #print(type((pickle.loads(i[f"data{j}"]))["embedding"]))
             print(i)
            
            


        
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
except OperationFailure as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


