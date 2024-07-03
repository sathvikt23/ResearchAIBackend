from flask import Flask, request, jsonify
import webscrape as web 
import chunks as ck
import embeddings as eb
import similarity as sm
import LoadLLM as llm
import db 

ET = web.ExtractText()
CK = ck.ChunksConversion()
LLM = llm.gemma("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")

app = Flask(__name__)

@app.route("/embeddings", methods=['POST'])
def generateEmbeddings():
    def UpdataUserData(username , dataname ):
        if (db.access.CheckUserData(username , dataname)==1):
            db.access.UpdateUserData(dataname, username)
        else :
            print("User and data already exists ")

    
    data = request.get_json()
    username = data.get("username")
    dataname = data.get("dataname")
    
    n = db.access.CheckDataName("CentralData", "embeddings", dataname)
    if n == 0:
        print("Already present")
        UpdataUserData(username,dataname)
        return jsonify({"message": "Data already present"}), 200
    

    else:
        print("Updating ....")
        pages_and_texts = ET.runlink(dataname)
        pages_and_chunks_over_min_token_len = CK.Convert(pages_and_texts)
        EB = eb.genrateEmbeddings("cuda")
        EB.get(dataname ,pages_and_chunks_over_min_token_len[0])
        UpdataUserData(username,dataname)
        return jsonify({"message": "Embeddings generation process completed"}), 200

@app.route("/getResponse", methods=["POST"])
def llmAnswers():
    data = request.get_json()
    query = data.get("query")
    username = data.get("username")
    
    SM = sm.search(username, "cuda")
    
    def Generate(query):
        scores_index_pages = SM.getEmbeddings(query)
        response = LLM.askGemma2(query, scores_index_pages[2], scores_index_pages[0], scores_index_pages[1])
        return response
    
    response = Generate(query)
    return jsonify({"message": response}), 200
    #return f"<h1>{response}</h1>", 200

if __name__ == '__main__':
    app.run()
