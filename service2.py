from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import similarity as sm
import db
import requests 
import neo4jgraph as neo
from py2neo import Graph, Node, Relationship
graph = Graph("neo4j+s://ffb0b9d5.databases.neo4j.io", auth=("neo4j", "v2WNDZxaDwNt9AVjLps6EZLvudLM5OoHPZFIBsGybvw"))
nj=neo.graphDB(graph)

app = FastAPI()

class jsonSchema(BaseModel):
    username: str
    query: str

@app.post("/getResponse")
async def llm_answers(request: jsonSchema):
    query = request.query
    username = request.username
    print("flag ")
    print(username)
    SM = sm.search(username, "cuda")
    def webcall(query,username ):
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
            return context
            
            
    print("flag ")
    def Generate(query):
        scores_index_pages = SM.getEmbeddings(query)
        print("flag ")
        min_score = 100
        max_score = 0
        for i in scores_index_pages[0]:
            score = i.cpu().item()
            if min_score > score:
                min_score = score
            if max_score < score:
                max_score = score
        print(max_score, min_score)

        if max_score > 0.20:
            print("in local rag")
            if (nj.checkQuery(query)):
                items=nj.breakQuery(query)
                finaldata=""
                for i in items :
                    scores_index_pages = SM.getEmbeddings(i)
                    min_score = 100
                    max_score = 0
                    print(i)
                    for i in scores_index_pages[0]:
                        score = i.cpu().item()
                        if min_score > score:
                            min_score = score
                        if max_score < score:
                            max_score = score
                    if max_score > 0.20:
                         context="- "+"\n-".join([item["sentence_chunk"] for item in scores_index_pages[2]])
                         context.replace("   "," ")
                         finaldata+=str(context[0:2000])
                    else:
                        finaldata+=str(webcall(query,username)[0:2000])
                print(finaldata)
                myobj = {   "text":finaldata,
                            "query": query
                        }
                x = requests.post('http://127.0.0.1:5400/process', json = myobj)
                y=x.json()
                print(type(y))
                result=y["result"]
                #response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
               
                myobj = {   "data":result,
                            "username": username,
                            "query": query
                        }
                x = requests.post('http://127.0.0.1:5100/askLLM', json = myobj)
                y=x.json()
                print(type(y))
                print(y)
                #response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
                return y["message"]



            else :


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
                #return response
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
