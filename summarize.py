from refextract import extract_references_from_string
import re
import spacy 
from spacy .lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import requests 
class sum:
    def references(data):
        k=extract_references_from_string(data)
        return k
        """for i in k:
    print(i["raw_ref"])"""
    

    def extract_equations(text):
        patterns = [
            # LaTeX commands
            r'\\frac\{[^}]*\}\{[^}]*\}',       # Fractions
            r'\\sqrt\{[^}]*\}',                 # Square roots
            r'\\int\{[^}]*\}',                  # Integrals
            r'\\sum\{[^}]*\}',                  # Summations
            r'\\prod\{[^}]*\}',                 # Products
            r'\\lim\{[^}]*\}',                  # Limits
            r'\\infty',                         # Infinity
            r'\\partial',                       # Partial derivatives
            r'\\nabla',                         # Nabla
            r'\\Delta',                         # Delta
            r'\\alpha|\\beta|\\gamma|\\delta|\\epsilon|\\zeta|\\eta|\\theta|\\iota|\\kappa|\\lambda|\\mu|\\nu|\\xi|\\pi|\\rho|\\sigma|\\tau|\\upsilon|\\phi|\\chi|\\psi|\\omega|\\Gamma|\\Lambda|\\Pi|\\Sigma|\\Phi|\\Psi|\\Omega',  # Greek letters
            r'∂[^\s=]*',                       # Partial derivatives
            r'\b(?:sin|cos|tan|cot|sec|csc|asin|acos|atan|acot|asec|acsc|P|E|Var|Cov|Pr)\b',  # Trigonometric and probability functions
            r'\b(?:log|ln|exp|max|min|sup|inf|arg|det|dim|gcd|lcm|mod)\b',  # Common mathematical functions
            r'[a-zA-Z_][a-zA-Z_0-9]*\(.*?\)',  # Functions with arguments
            r'\b\d+\.?\d*\b',                  # Numbers (integers and decimals)
            r'\d+\.\d+e[\+\-]?\d+',            # Scientific notation
            r'[+\-*/^=(),{}\[\]|<>]',          # Mathematical operators and symbols
            r'\b(?:\w+)\b',                    # Variables or standalone words
            r'∞|∫|∑|∏|∆|∇',                   # Special mathematical symbols
            r'[\u2200-\u22FF]+',               # Unicode mathematical symbols
            r'\b\d+\.?\d*',                    # Basic numbers
            r'\b\w+',                          # Variables
            r'[+\-\*/\^\=\(\)\{\}\[\]]',      # Operators and brackets
            r'∂[^\s=]+',                       # Partial derivatives
            r'\\frac\{[^}]*\}\{[^}]*\}',       # LaTeX fractions
            r'\b\d+\.\d+\b',                  # Decimal numbers
            r'[a-zA-Z_][a-zA-Z_0-9]*\(.*?\)',  # Functions with arguments
            r'\b(?:sin|cos|tan|cot|sec|csc|asin|acos|atan|acot|asec|acsc|P|E|Var|Cov|Pr)\b',  # Trigonometric and probability functions
            r'P\s*\(.*?\)\s*=\s*[^,\)]+',     # Probability formulas
            r'[A-Za-z]+\s*=\s*[0-9\+\-\*/\(\)XxYy]+',  # General equations
            r'\b[0-9]+\s*=\s*[0-9\+\-\*/\(\)XxYy]+',  # Equations starting with numbers
            r'[A-Za-z]+\s*\(\s*[A-Za-z]+\s*\)\s*=\s*[0-9\+\-\*/\(\)]+',  # Function definitions
            r'[A-Za-z]+\s*\(\s*[A-Za-z]+\s*\)\s*=\s*[A-Za-z\+\-\*/\(\)]+',  # Functions with variables
            r'[A-Za-z]+\s*\+\s*[A-Za-z]+\s*=\s*[A-Za-z0-9\+\-\*/\(\)]+',  # Equations with multiple variables
            r'\b\[\s*[^\]]+\s*\]\s*=\s*[0-9\+\-\*/\(\)XxYy]+\b',  # Matrix/vector equations
            r'\b\{\s*[^\}]+\s*\}\s*=\s*[0-9\+\-\*/\(\)XxYy]+\b',  # Set equations
            r'\b\(\s*[^\)]+\s*\)\s*=\s*[0-9\+\-\*/\(\)XxYy]+\b',  # Parentheses enclosed equations
            r'[A-Za-z]+\s*:\s*[0-9\+\-\*/\(\)XxYy]+',  # Ratio or colon expressions
            r'[A-Za-z]+\s*<\s*[0-9\+\-\*/\(\)XxYy]+',  # Inequalities
            r'[A-Za-z]+\s*>\s*[0-9\+\-\*/\(\)XxYy]+',  # Inequalities
            r'[A-Za-z]+\s*<=\s*[0-9\+\-\*/\(\)XxYy]+',  # Inequalities
            r'[A-Za-z]+\s*>=\s*[0-9\+\-\*/\(\)XxYy]+',  # Inequalities
            r'\b\|.*?\|\s*=\s*[0-9\+\-\*/\(\)XxYy]+\b',  # Norms or absolute value
            r'\b[A-Za-z]+\s*=\s*\{\s*[A-Za-z0-9\+\-\*/\(\)\|]+\s*\}',  # Set definitions
            r'\b\int\s*[^\s]+\s*d[^\s]+',  # Integration
            r'\b\frac\{[^\}]+\}\{[^\}]+\}',  # Fractions
            r'\b\d+dx',  # Differential elements
            r'\b\lim_{[^\}]+}\s*[^\s]+',  # Limit notation
            r'\b\sum_{[^\}]+}\s*\w+'  # Summation notation
        ]

        # Combine patterns into a single regex pattern
        #pattern = re.compile(r'\b\d+\.?\d*|\b\w+|[\+\-\*/\^\=\(\)\{\}\[\]]|∂[^\s=]+|\\frac\{[^}]*\}\{[^}]*\}|\b\d+\.\d+\b|[a-zA-Z_][a-zA-Z_0-9]*\(.*?\)|\b(?:sin|cos|tan|cot|sec|csc|asin|acos|atan|acot|asec|acsc|P|E|Var|Cov|Pr)\b')
        pattern=re.compile(r'\\sqrt\{[^}]*\}')
        # Compile the regex pattern with verbose flag
        equations=" "
        for i in patterns:
            try:
                  pattern=re.compile(i)
                  temp=pattern.findall(text) 
                  if (len(temp)>0):
                       for i in temp :
                            equations+=i
                       
                  #print(i)
            except:
                  pass

        # Join matched par return equations

        
        myobj = {   "data":"",
                                            "username": "Sathvik",
                                            "query": """"
                                            ***instructions***
                                            Reframe the mathematical expressions only which are understandable
                                            Keep the heading as Math Functions 
                                            \n content:"""+equations
        }
        x = requests.post('http://127.0.0.1:5100/askLLM', json = myobj)
            
        y=x.json()
        print(type(y))
        return  y["message"]

    def getsentence(data):#Give data in the string format and no of requried lines 
                lines=10
                stopwords=list(STOP_WORDS)
                nlp=spacy.load('en_core_web_sm')
                docx=nlp(data)
                wordFrequencies={}
                for word in docx:
                    if word.text not in stopwords:
                        if word.text not in wordFrequencies.keys():
                            wordFrequencies[word.text]=1
                        else:
                            wordFrequencies[word.text]+=1

                maximumfreq=max(wordFrequencies.values())
                for word in wordFrequencies.keys():
                    wordFrequencies[word]=(wordFrequencies[word]/maximumfreq) 
                sentencelist=[sentence for sentence in docx.sents]
                sentencescores={}
                for sent in sentencelist:
                    for word in sent :
                        if word.text.lower() in wordFrequencies.keys():
                            if len(sent.text.split(' '))<30:
                                if sent not in sentencescores.keys():
                                    sentencescores[sent]=wordFrequencies[word.text.lower()]
                                else:
                                    sentencescores[sent]+=wordFrequencies[word.text.lower()]
                #print(sentencescores)
             

                summarized=nlargest(lines,sentencescores,key=sentencescores.get)
                final=""
                for i in summarized:
                    final+=str(i)
                return final 
    def getall3(text):
# Example usage

            finaldata=""
            data1=sum.getsentence(text)

            data2=sum.extract_equations(text)
            data3=sum.references(text)
            #print(data1)
            finaldata+=data1
            finaldata+="Math Formulas :\n"
            for i in data2 :
                finaldata+=i
            finaldata+="References :\n"
            finaldata2=""
            for i in data3:
                if (len(i.keys())>2):
                    finaldata2+=i["raw_ref"][0]
            print(data1)
            print("-------------------------")
            print(data2)
            print("-------------------------")
            for i in data3:
                if ("author" in i.keys()):
                    print(i["raw_ref"][0])
            myobj = {   "data":"",
                                    "username": "Sathvik",
                                    "query": """"Enhance the Summary and the Math Formulas . \n Content :"""+finaldata
                                }
            x = requests.post('http://127.0.0.1:5100/askLLM', json = myobj)
            y=x.json()
            print(type(y))
            finaldata=y["message"]
            finaloutput=finaldata.replace("<bos>"," ")
            finaloutput=finaloutput.replace("<eos>"," ")
            if (finaldata2!=""):
                 return finaloutput+"References \n"+finaldata2
    
            return finaloutput
