from py2neo import Graph, Node, Relationship
import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import LoadLLM as LLM

class graphDB:
    def _init_(self, graph):
        self.graph = graph

    def create_nodes_and_relationships(self, data):
        for item in data:
            node1 = Node("Data", name=item['node'])
            node2 = Node("Data", name=item['chunk'])
            relationship = Relationship(node1, "RELATED_TO", node2, relation=item['edge'])
            graph.merge(node1, "Data", "name")
            graph.merge(node2, "Data", "name")
            graph.merge(relationship)

    def ask_question(self, question):
        query = f"""
            MATCH (a:Data)
            WHERE toLower(a.name) = toLower('{question}')
            MATCH (a)-[r:RELATED_TO]->(b:Data)
            RETURN r.relation AS relation
        """
        result = graph.run(query).data()
        answer = ""
        for relation in result:
            answer += relation['relation'] + " "
        return answer.strip()

    def llm_query_gen(self, text, LLM):
        graph_ask = '''You are a network graph maker who extracts terms and their relations from a given context. 
                    You are provided with a context chunk (delimited by ). Your task is to extract the ontology 
                    of terms mentioned in the given context. These terms should represent the key concepts as per the context.
                    Thought 1: While traversing through each sentence, think about the key terms mentioned in it.
                        Terms may include object, entity, location, organization, person, 
                        condition, acronym, documents, service, concept, etc.
                        Terms should be as atomistic as possible
                    Thought 2: Think about how these terms can have one-on-one relation with other terms.
                        Terms that are mentioned in the same sentence or the same paragraph are typically related to each other.
                        Terms can be related to many other terms
                    Thought 3: Find out the relation between each such related pair of terms.
                    Format your output as a list of json. Each element of the list contains a pair of terms
                    and the relation between them, like the following: 
                    [
                    {
                        "node": "A concept from extracted ontology",
                        "chunk": "A related concept from extracted ontology",
                        "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"
                    }, {...}
                    ]'''
        response = LLM.askGemma1(graph_ask + text)
        data = json.loads(response)
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

    def query_processor(self, text, query, LLM):
        self.llm_query_gen(text, LLM)
        relevant_ans = self.retrieve_relevant_data_from_graph(query)
        return relevant_ans

    def delete_nodes_and_relationships(self):
        query = "MATCH (n) DETACH DELETE n"
        graph.run(query)
        print("nodes and relationships deleted")

graph = Graph("neo4j+s://ffb0b9d5.databases.neo4j.io", auth=("neo4j", "v2WNDZxaDwNt9AVjLps6EZLvudLM5OoHPZFIBsGybvw"))
db = graphDB(graph)