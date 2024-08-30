from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import LoadLLM as llm
import similarity as sm
import webscrape as web 
import embeddings as eb
import chunks as ck
LLM = llm.gemma("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")
CK = ck.ChunksConversion()
EB = eb.genrateEmbeddings("cuda")
ET = web.ExtractText()
app = FastAPI()

class jsonSchema(BaseModel):
    query:str
    username :str
    data :str

@app.post("/askLLM")
def llmAnswers(request:jsonSchema):
    query=request.query
    username=request.username
    data=request.data
    SM = sm.search(username, "cuda")
    if (data==""):
        print("null")
        response =LLM.askGemma1(query)
        return ({"message":response })
    else :
        def Generate(query):
            response=LLM.askGemma2(query,data)
            return response 


        response = Generate(query)
        return {"message": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5100)
