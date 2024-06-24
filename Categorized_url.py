from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.telegram import text_to_docs

loader = WebBaseLoader("https://python.langchain.com/v0.2/docs/integrations/document_loaders/web_base/")
data = loader.load()

cleaned_data = []
for document in data:
    cleaned_text = document.page_content.replace('\n', '')
    cleaned_text = cleaned_text.replace('\\n', '')  # Remove '\\n' as well if present
    cleaned_documents = text_to_docs(cleaned_text)
    cleaned_data.extend(cleaned_documents)

cleaned_data