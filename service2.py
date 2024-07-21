from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import similarity as sm
import db
import requests 
app = FastAPI()

class jsonSchema(BaseModel):
    username: str
    query: str

@app.post("/getResponse")
async def llm_answers(request: jsonSchema):
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
        if min_score > 0.10 and max_score > 0.10:
            print("in local rag")
            
            context="- "+"\n-".join([item["sentence_chunk"] for item in scores_index_pages[2]])
            context.replace("   "," ")
            myobj = {   "data":context,
                         "username": username,
                           "query": query
                    }
            x = requests.post('http://127.0.0.1:5100/askLLM', json = myobj)
            y=x.json()
            print(type(y))
            print(y)
            #response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
            return y["message"]
            return response
        else:
            myobj = {   
                         "username": username,
                           "query": query
                    }
            x = requests.post('http://127.0.0.1:5300/webEmbeddings', json = myobj)
            y=x.json()
            print(y)
            scores_index_pages = SM.getEmbeddings(query)
            context="- "+"\n-".join([item["sentence_chunk"] for item in scores_index_pages[2]])
            context.replace("   "," ")
            myobj = {   "data":context,
                         "username": username,
                           "query": query
                    }
            x = requests.post('http://127.0.0.1:5100/askLLM', json = myobj)
            y=x.json()
            print(type(y))
            print(y)
            
            return y["message"]
    response = Generate(query)
    return {"message": response}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5200)
