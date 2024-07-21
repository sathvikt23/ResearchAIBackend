from py2neo import Graph, Node, Relationship, NodeMatcher
import json
import spacy 
from spacy .lang.en.stop_words import STOP_WORDS



textjson = [
    {'node': 'Macronutrients', 'chunk': 'large amounts', 'edge': 'Macronutrients are nutrients that are needed in large amounts.'},
    {'node': 'Macronutrients', 'chunk': 'carbohydrates', 'edge': 'Macronutrients can be categorized into three classes: carbohydrates, lipids, and proteins.'},
    {'node': 'Proteins', 'chunk': 'macronutrient', 'edge': 'Proteins are one of the three classes of macronutrients.'},
    {'node': 'Carbohydrates', 'chunk': 'macronutrient', 'edge': 'Carbohydrates are one of the three classes of macronutrients.'},
    {'node': 'Lipids', 'chunk': 'macronutrient', 'edge': 'Lipids are one of the three classes of macronutrients.'},
    {'node': 'Macronutrients', 'chunk': 'cellular energy', 'edge': 'Macronutrients can be metabolically processed into cellular energy.'},
    {'node': 'Cellular energy', 'chunk': 'chemical bonds', 'edge': 'The energy from macronutrients comes from their chemical bonds.'},
    {'node': 'Cellular energy', 'chunk': 'work', 'edge': 'Cellular energy is converted into cellular energy that is then utilized to perform work.'},
    {'node': 'Cellular energy', 'chunk': 'basic functions', 'edge': 'Cellular energy is utilized to perform work, allowing our bodies to conduct their basic functions.'},
    {'node': 'Food energy', 'chunk': 'calorie', 'edge': 'A unit of measurement of food energy is the calorie.'},
    {'node': 'Calories', 'chunk': 'nutrition food labels', 'edge': 'On nutrition food labels the amount given for “calories” is actually equivalent to each calorie multiplied by one thousand.'},
    {'node': 'Kilocalorie', 'chunk': 'nutrition food labels', 'edge': 'A kilocalorie (one thousand calories, denoted with a small “c”) is synonymous with the “Calorie” (with a capital “C”) on nutrition food labels.'},
    {'node': 'Macronutrient', 'chunk': 'water', 'edge': 'Water is also a macronutrient in the sense that you require a large amount of it.'},
    {'node': 'Macronutrients', 'chunk': 'calories', 'edge': 'Unlike the other macronutrients, water does not yield calories.'}
]

uri = ""
username = ""
password = ""
graph = Graph(uri, auth=(username, password))

class neo:
      def create_nodes_and_relationships(data):
        for item in data:
            node1 = Node("Data", name=item['node'])
            node2 = Node("Data", name=item['chunk'])
            relationship = Relationship(node1, "RELATED_TO", node2, relation=item['edge'])
            graph.merge(node1, "Data", "name")
            graph.merge(node2, "Data", "name")
            graph.merge(relationship, "Data", "name")

      def askquestion(question):
            query = f"""
                        MATCH (a:Data)
                        WHERE toLower(a.name) = toLower('{question}')
                        MATCH (a)-[r:RELATED_TO]->(b:Data)
                        RETURN r.relation AS relation
                    """
            result = graph.run(query).data()
            answer=""
            for relation in result:
                answer += relation['relation']
            
            return answer
      
      def llmQueryGen(text,LLM):
           #text="- "+"\n-".join([item["sentence_chunk"] for item in text])
           graphAsk='''You are a network graph maker who extracts terms and their relations from a given context. "
                    "You are provided with a context chunk (delimited by ) Your task is to extract the ontology "
                    "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
                    "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
                    "\tTerms may include object, entity, location, organization, person, \n"
                    "\tcondition, acronym, documents, service, concept, etc.\n"
                    "\tTerms should be as atomistic as possible\n\n"
                    "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
                    "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
                    "\tTerms can be related to many other terms\n\n"
                    "Thought 3: Find out the relation between each such related pair of terms. \n\n"
                    "Format your output as a list of json. Each element of the list contains a pair of terms"
                    "and the relation between them, like the follwing: \n"
                    "[\n"
                    "   {\n"
                    '       "node": "A concept from extracted ontology",\n'
                    '       "chunk": "A related concept from extracted ontology",\n'
                    '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
                    "   }, {...}\n"
                    "]'''
           response=LLM.askGemma3(graphAsk+text)
           data=f'{response}'
           print("===========================================")
           print(data)
           

      def retrieve_relevantData_from_graph(query):
            stopwords=list(STOP_WORDS)
            nlp=spacy.load('en_core_web_sm')
            docx=nlp("what are macronutrients and vitamins")
            wordFrequencies={}
            for word in docx:
                if word.text not in stopwords:
                     if word.text not in wordFrequencies.keys():
                         wordFrequencies[word.text]=1
                     else:
                         wordFrequencies[word.text]+=1
            retrievedData=""
            for i in wordFrequencies.keys():
                d=graph.askquestion(i)
                if d==None or d=="":
                    pass
                else:
                    retrievedData+=d
            return retrievedData
        

stopwords=list(STOP_WORDS)
nlp=spacy.load('en_core_web_sm')
docx=nlp("what are macronutrients and vitamins")
wordFrequencies={}
for word in docx:
     if word.text not in stopwords:
         if word.text not in wordFrequencies.keys():
            wordFrequencies[word.text]=1
         else:
                wordFrequencies[word.text]+=1
retrievedData=""
for i in wordFrequencies.keys():
        retrievedData+=i+"/"
print(retrievedData.lower())