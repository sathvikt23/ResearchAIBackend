from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import webscrape as web
import chunks as ck
import embeddings as eb
import db
import spacy 
from spacy .lang.en.stop_words import STOP_WORDS

app = FastAPI()

class EmbeddingRequest(BaseModel):
    username: str
    dataname: str

class webEmbedding(BaseModel):
    username :str 
    query: str 


EB = eb.genrateEmbeddings("cuda")
ET = web.ExtractText()
CK = ck.ChunksConversion()


@app.post("/embeddings")
def generate_embeddings(request: EmbeddingRequest):
    username = request.username
    dataname = request.dataname

    def UpdataUserData(username, dataname):
        if db.access.CheckUserData(username, dataname) == 1:
            db.access.UpdateUserData(dataname, username)
        else:
            print("User and data already exists")

    n = db.access.CheckDataName("CentralData", "embeddings", dataname)
    if n == 0:
        print("Already present")
        UpdataUserData(username, dataname)
        return {"message": "Embeddings already present"}
        
    else:
        print("Updating ....")
        pages_and_texts = ET.runlink(dataname)
        pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
        EB.get(dataname, pages_and_chunks_over_min_token_len[0])
        UpdataUserData(username, dataname)
        return {"message": "Embeddings generation process completed"}
    

@app.post("/webEmbeddings")
def webrag_embeddings(request :webEmbedding):
    username = request.username
    query = request.query
    stopwords=list(STOP_WORDS)
    nlp=spacy.load('en_core_web_sm')
    docx=nlp(query)
    wordFrequencies={}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in wordFrequencies.keys():
                wordFrequencies[word.text]=1
            else:
                    wordFrequencies[word.text]+=1
    dataname=""
    for i in wordFrequencies.keys():
            dataname+=i+"/"
    dataname=dataname.lower()
    def UpdataUserData(username, dataname):
        if db.access.CheckUserData(username, dataname) == 1:
            db.access.UpdateUserData(dataname, username)
        else:
            print("User and data already exists")

    n = db.access.CheckDataName("CentralData", "embeddings", dataname)
    if n == 0:
        print("Already present")
        UpdataUserData(username, dataname)
        return {"dataname": dataname}
        
    else:
        print("Updating ....")
        pages_and_texts = ET.serp(query)
        pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
        EB.get(dataname, pages_and_chunks_over_min_token_len[0])
        UpdataUserData(username, dataname)
        return {"dataname": dataname}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5300)