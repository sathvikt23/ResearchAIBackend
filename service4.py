from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from py2neo import Graph, Node, Relationship
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

app = FastAPI()

# Initialize the Graph Database connection
graph = Graph("neo4j+s://ffb0b9d5.databases.neo4j.io", auth=("neo4j", "v2WNDZxaDwNt9AVjLps6EZLvudLM5OoHPZFIBsGybvw"))

class GraphDB:
    def __init__(self, graph):
        self.graph = graph

    def break_query(self, query):
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        docx = nlp(query)
        word_frequencies = {}
        for word in docx:
            if word.text.lower() not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

        data = [i for i in word_frequencies.keys()]
        return data

    def check_query(self, query):
        words_list = [
            # Interrogative Words
            "which", "how", "how much", "how many",
            # Comparison Words
            "more", "less", "better", "worse", "as", "than",
            # Differentiating Words
            "different", "difference", "differ", "contrast", "unlike",
            "distinct", "distinctive", "varies", "variation", "opposite",
            "versus", "compare", "contradict", "varied", "distinction",
            "similar", "same", "dissimilar", "between", "among", "within",
            "across", "relative to", "in comparison to", "in contrast to",
            # Synonyms
            "distinct", "unlike", "diverse", "varied", "distinction",
            "disparity", "variation", "contrast", "differ", "change",
            "modulates", "reverse", "antithesis", "against", "compared to",
            "in contrast to", "oppose", "deny", "dispute", "assorted",
            "identical", "equal", "resembling", "divergent",
            # Conjunctions
            "are", "and", "or", "but", "nor", "for", "yet", "so",
            "although", "because", "since", "unless", "if", "while",
            "whereas", "as long as", "even though", "provided that", "whether"
        ]
        count = 0
        query = query.lower()
        for i in words_list:
            count += query.count(i)

        return count > 2

    def create_nodes_and_relationships(self, data):
        for item in data:
            node1 = Node("Data", name=item['node'])
            node2 = Node("Data", name=item['chunk'])
            relationship = Relationship(node1, "RELATED_TO", node2, relation=item['edge'])
            self.graph.merge(node1, "Data", "name")
            self.graph.merge(node2, "Data", "name")
            self.graph.merge(relationship)

    def ask_question(self, question):
        query = f"""
            MATCH (a:Data)-[r:RELATED_TO]->(b:Data)
            WHERE toLower(a.name) = toLower('{question}') 
                OR toLower(b.name) = toLower('{question}')
            RETURN a.name AS node_a, b.name AS node_b, r.relation AS relation
        """
        result = self.graph.run(query).data()
        answer = " ".join([relation['relation'] for relation in result])
        return answer.strip()

    def extract_relations(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        data = []

        for sent in doc.sents:
            chunks = list(sent.noun_chunks)
            if not chunks:
                continue  # Skip sentences with no noun chunks

            node = chunks[0].root.text
            for chunk in chunks[1:]:
                data.append({
                    "node": node,
                    "chunk": chunk.root.text,
                    "edge": sent.text.strip()
                })

        self.create_nodes_and_relationships(data)

    def retrieve_relevant_data_from_graph(self, query):
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        docx = nlp(query)
        word_frequencies = {}
        for word in docx:
            if word.text.lower() not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

        retrieved_data = ""
        for i in word_frequencies.keys():
            d = self.ask_question(i)
            if d:
                retrieved_data += d + " "

        return retrieved_data.strip()

    def query_processor(self, text, query):
        self.extract_relations(text)
        relevant_ans = self.retrieve_relevant_data_from_graph(query)
        self.delete_nodes_and_relationships()
        return relevant_ans

    def delete_nodes_and_relationships(self):
        query = "MATCH (n) DETACH DELETE n"
        self.graph.run(query)
        print("nodes and relationships deleted")

# Create an instance of the GraphDB class
db = GraphDB(graph)

class QueryRequest(BaseModel):
    text: str
    query: str

@app.post("/process")
async def process_query(request: QueryRequest):
    try:
        result = db.query_processor(request.text, request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5400)
