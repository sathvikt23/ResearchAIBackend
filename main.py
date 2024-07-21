from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import webscrape as web
import chunks as ck
import embeddings as eb
import similarity as sm
import LoadLLM as llm
import db
import neo4jgraph as nj

app = FastAPI()

class EmbeddingRequest(BaseModel):
    username: str
    dataname: str

class QueryRequest(BaseModel):
    query: str
    username: str

EB = eb.genrateEmbeddings("cuda")
ET = web.ExtractText()
CK = ck.ChunksConversion()
LLM = llm.gemma("hf_token")

@app.post("/embeddings")
async def generate_embeddings(request: EmbeddingRequest):
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

@app.post("/getResponse")
async def llm_answers(request: QueryRequest):
    query = request.query
    username = request.username

    SM = sm.search(username, "cuda")

    def Generate(query):
        scores_index_pages = SM.getEmbeddings(query)

        min_score = 100
        max_score = 0
        for i in scores_index_pages[0]:
            score = i.cpu().item()
            if min_score > score:
                min_score = score
            if max_score < score:
                max_score = score
        print(max_score, min_score)
        if min_score > 0.20 and max_score > 0.20:
            print("in local rag")
            response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return response
        else:
            pages_and_texts = ET.serp(query)
            pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
            WebData = EB.get2(pages_and_chunks_over_min_token_len[0])
            scores_index_pages = SM.getEmbeddings2(query, WebData)
            response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return response

    response = Generate(query)
    return {"message": response}

@app.post("/getResponseNeo")
async def Neollm_answers(request: QueryRequest):
    query = request.query
    username = request.username

    SM = sm.search(username, "cuda")

    def Generate(query):
        scores_index_pages = SM.getEmbeddings(query)

        min_score = 100
        max_score = 0
        for i in scores_index_pages[0]:
            score = i.cpu().item()
            if min_score > score:
                min_score = score
            if max_score < score:
                max_score = score
        print(max_score, min_score)
        if min_score > 0.1 and max_score > 0.1:
            print("in local rag")
            nodes = nj.neo.llmQueryGen(scores_index_pages[2], LLM)
            print(nodes)
            nj.neo.create_nodes_and_relationships(nodes)
            data = nj.neo.retrieve_relevantData_from_graph(query)
            response = LLM.askGemma2(query, data, scores_index_pages[0], scores_index_pages[1])

            return response
        else:
            pages_and_texts = ET.serp(query)
            pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
            WebData = EB.get2(pages_and_chunks_over_min_token_len[0])
            scores_index_pages = SM.getEmbeddings2(query, WebData)
            response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return response

    response = Generate(query)
    return {"message": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
