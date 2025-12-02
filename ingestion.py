from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

# folder where THIS file (ingestion.py) lives
BASE_DIR = Path(__file__).resolve().parent

pdf_path = BASE_DIR / "doc" / "corrective_rag.pdf"

loader = PyPDFLoader(str(pdf_path))
doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=0
)

doc_splits = text_splitter.split_documents(doc)

# comment out because we just need did once only
# vectorstore = Chroma.from_documents(
#     documents=doc_splits,
#     collection_name="rag-chroma",
#     embedding=OpenAIEmbeddings(),
#     persist_directory=".chroma"
# )

vectorstore_read = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
)

vector_store_size = vectorstore_read._collection.count()
print(f"Vector store size: {vector_store_size}")

# Get the retriever
retriever = vectorstore_read.as_retriever()

if __name__ == "__main__":
    load_dotenv()
    # Get the number of documents stored
    vector_store_size = vectorstore_read._collection.count()
    print(f"Vector store size: {vector_store_size}")

    question = "what is corrective RAG?"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    print(len(docs))
    print(doc_txt)