import os
import requests
import fitz
from tqdm.auto import tqdm
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi as yta
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.telegram import text_to_docs
from serpapi import GoogleSearch
import os
class ExtractText:
    
    def init(self):
         print("intialized")
    def text_formatter(self,text:str)->str:
        cleaned_text=text.replace("\n"," ").strip()
        return cleaned_text
    def open_and_read_pdf(self,pdf_path:str)->list[dict]:
        doc =fitz.open(pdf_path)
        print(type(doc))
        pages_and_texts=[]
        for page_number , page in  tqdm (enumerate (doc)):
            text =page.get_text()
            text=self.text_formatter(text=text)
            pages_and_texts.append(
                {"page_number":page_number-41,
                "page_char_count":len(text),
                "page_word_count":len(text.split(" ")),
                "page_sentence_count_raw":len(text.split(". ")),
                "page_token_count":len(text)/4,
                "text":text}
            )
        return pages_and_texts
    def urlDownloadLink(self,url):
        dummy=url
        data=(dummy.split("//"))
        data=" ".join(data).split("/")
        data=data[1]
        pdf_path=data+".pdf"

        if not os.path.exists(pdf_path):
                print(f"not found ")
                filename=pdf_path
                response= requests.get(url)
                if response.status_code== 200:
                    with open(filename,"wb") as file :
                        file.write(response.content )
                    print(f"the file has be taken {filename }")
                    pages_and_texts=self.open_and_read_pdf(pdf_path=pdf_path)
                    return pages_and_texts
                else :
                    print(f"the file has be failed  {filename }")
                    return
        else:
                print("file exists ")
                pages_and_texts=self.open_and_read_pdf(pdf_path=pdf_path)
                return pages_and_texts
    def rawtext(self,info):
            print(len(info))
            pages_and_texts=[]
           
            # Split text into "pages" for demonstration purposes
            pages =[info[i:i+2000] for i in range(0,len(info),2000)]  # Split by double newline for simplicity
            
            for page_number, page_text in tqdm(enumerate(pages), desc="Processing Text"):
                formatted_text = str(page_text)
                pages_and_texts.append({
                    "page_number": page_number + 1,  # Adjust page number as needed
                    "page_char_count": len(formatted_text),
                    "page_word_count": len(formatted_text.split()),
                    "page_sentence_count_raw": len(formatted_text.split(". ")),
                    "page_token_count": len(formatted_text.split()) / 4,
                    "text": formatted_text
                })
            
            return pages_and_texts

    def transcribe(self,link):#Here pass the link only , copy it from the url
                    ids=link.split("=")
                    vid_id=ids[1]
                    data=yta.get_transcript(vid_id)
                    transcript=''
                    for value in data:
                        for key,val in value.items():
                            if key=="text":
                                transcript+=val

                    l=transcript.splitlines()
                    finaldata=" ".join(l)
                    return self.rawtext(finaldata)

    def webscrape(self,link):

        os.environ['USER_AGENT'] = str(link)

        loader = WebBaseLoader(link)
        data = loader.load()

        cleaned_data = []
        for document in data:
            cleaned_text = document.page_content.replace('\n', '')
            cleaned_text = cleaned_text.replace('\\n', '')  # Remove '\\n' as well if present
            cleaned_documents = text_to_docs(cleaned_text)
            cleaned_data.extend(cleaned_documents)

        return cleaned_data
    
    def webRAG(self,links):
         finaldata=""
         for i in links:
              data=self.webscrape(i)
              for i in data :
                   finaldata+=(list(i)[0][1])

         finaldata=finaldata.replace("\xa0","")
         finaldata=finaldata.replace("‚Äî","")
         return self.rawtext(str(finaldata))
    def serp(self,query):
         params = {
            "api_key": "df39187b734f04b75757c1500190491c6b45f9db901d4d466837053854b4329d",
            "engine": "google",
            "q": query,
             "location": "India",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en"
            }
         search = GoogleSearch(params)
         results = search.get_dict()
         data=results["organic_results"]
         links=[]
         for i in data:
            links.append(i["link"])
         return self.webRAG(links)
              
              

    def runlink(self,given_link):
         if "youtube.com/watch?v" in given_link:
             return self.rawtext(self.transcribe(given_link))
         elif "/open/download?type=pdf" in given_link:
              return self.urlDownloadLink(given_link)
         else:
           
              data=self.webscrape(given_link)
              finaldata=""
              for i in data :
                   finaldata+=(list(i)[0][1])
              finaldata=finaldata.replace("\xa0","")
              finaldata=finaldata.replace("‚Äî","")

              return self.rawtext(str(finaldata))
            

