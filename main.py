from fastapi import FastAPI, Request
from pydantic import BaseModel
import webscrape as web
import chunks as ck
import embeddings as eb
import similarity as sm
import LoadLLM as llm
import db
EB = eb.genrateEmbeddings("cuda")
ET = web.ExtractText()
CK = ck.ChunksConversion()
LLM = llm.gemma("hf_token")

app = FastAPI()

class EmbeddingsRequest(BaseModel):
    username: str
    dataname: str

class QueryRequest(BaseModel):
    query: str
    username: str

@app.post("/embeddings")
async def generate_embeddings(request: EmbeddingsRequest):
    def UpdataUserData(username, dataname):
        if db.access.CheckUserData(username, dataname) == 1:
            db.access.UpdateUserData(dataname, username)
        else:
            print("User and data already exists")

    username = request.username
    dataname = request.dataname

    n = db.access.CheckDataName("CentralData", "embeddings", dataname)
    if n == 0:
        print("Already present")
        UpdataUserData(username, dataname)
        return {"message": "Data already present"}

    else:
        print("Updating ....")
        pages_and_texts = ET.runlink(dataname)
        pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
        EB = eb.genrateEmbeddings("cuda")
        EB.get(dataname, pages_and_chunks_over_min_token_len[0])
        UpdataUserData(username, dataname)
        return {"message": "Embeddings generation process completed"}

@app.post("/getResponse")
async def llm_answers(request: QueryRequest):
    query = request.query
    username = request.username

    SM = sm.search(username, "cuda")

    def Generate(query):
        scores_index_pages = SM.getEmbeddings(query)
        
        min=100
        max=0
        for i in scores_index_pages[0]:
            score=i.cpu().item()
            if min>score:
               min=score
            if max<score:
                max=score
        print(max , min )
        if (min>0.20 and max >0.20):
            print("in local rag")
            response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return response
        else:
            pages_and_texts=ET.serp(query)
            pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
            WebData=EB.get2(pages_and_chunks_over_min_token_len[0])
            scores_index_pages = SM.getEmbeddings2(query,WebData)
            response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return response

    response = Generate(query)
    return {"message": response}
    # return f"<h1>{response}</h1>"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
