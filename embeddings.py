import os 
import requests
import fitz
from tqdm.auto import tqdm
import json 
import pickle
import pandas as pd 
#new1
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import db 
# MongoDB connection details
atlas_url = 'mongodb+srv://sathvikt23a:rKRC5yAGpbiSvhuD@cluster0.8dtd3nj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

import re 
import pandas as pd 
from spacy.lang.en import English
nlp=English()
nlp.add_pipe("sentencizer")
from sentence_transformers import SentenceTransformer
from sentence_transformers import  util
class genrateEmbeddings:
    embedding_model=SentenceTransformer(model_name_or_path="all-mpnet-base-v2")
    pages_and_chunks_over_min_token_len2=[]
    text_chunks_embeddings=[]
    def __init__(self , Device ):
        #embedding_model=SentenceTransformer(model_name_or_path="all-mpnet-base-v2",device=Device)
        self.embedding_model.to(Device) # requires  GPU installed, for reference on my local machine, I'm using a NVIDIA RTX 4060
    def get(self ,dataname ,pages_and_chunks_over_min_token_len):
        self.pages_and_chunks_over_min_token_len2=pages_and_chunks_over_min_token_len
        for item in tqdm(pages_and_chunks_over_min_token_len):
          item["embedding"] = self.embedding_model.encode(item["sentence_chunk"])
        #text_chunks=[item["sentence_chunk"] for item in pages_and_chunks_over_min_token_len]
        #print(text_chunks[420])
        #text_chunks_embeddings=self.embedding_model.encode(text_chunks,batch_size=12,convert_to_tensor=True)
        db.access.UpdateEmbedding(dataname,self.pages_and_chunks_over_min_token_len2)
        print("---------------------------------------------------------")
        #print(text_chunks_embeddings)

    def saveToCsv(self):
        print("---------------------------------------------------------")
        print(self.pages_and_chunks_over_min_token_len2)
        text_chunks_and_embeddings_df=pd.DataFrame(self.pages_and_chunks_over_min_token_len2)
        embeddings_df_save_path="text_chunks_and_embeddings_df.csv"
        text_chunks_and_embeddings_df.to_csv(embeddings_df_save_path, index =False )
        print("++++++++++++++++++++++++")
        
        client = MongoClient(atlas_url)
        database = client['solutiondata']
        collection= database['a']
        db.access.UpdateEmbedding("health",self.pages_and_chunks_over_min_token_len2)
        # Query for a movie that has the title 'Back to the Future'
        """query = {'title': 'Back to the Future'}
        j=0
        for i in self.pages_and_chunks_over_min_token_len2:
         collection.insert_one({f"data{j}":pickle.dumps(i)})
         print(j)
         j=j+1"""
       
       
        return embeddings_df_save_path