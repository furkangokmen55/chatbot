from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

load_dotenv()

# PDF dosyalarının bulunduğu klasör
pdf_folder = "./pdfs"  # klasör adını ihtiyacına göre değiştir

# Tüm PDF dosyalarını yükle
pdf_paths = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

docs = []
for path in pdf_paths:
    loader = PyPDFLoader(path)
    docs.extend(loader.load())

docs_list =docs

"""
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
"""
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
     documents=doc_splits,
     collection_name="rag-chroma",
     embedding=OpenAIEmbeddings(),
     persist_directory="./.chroma",
 )

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever()