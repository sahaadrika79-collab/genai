from langchain_community.document_loaders import TextLoader

loader = TextLoader("Document_loader/note.txt")  

docs = loader.load()

print(docs[0].page_content)