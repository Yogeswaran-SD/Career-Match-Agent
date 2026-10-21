
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from llm import create_llm

def process_pdf(file_path: str = "yogi_resume.pdf"):
    loader = PyPDFLoader(file_path)
    document = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 50
    )
    chunks = splitter.split_documents(document)
    return chunks


embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2") 

vectors = Chroma(
        embedding_function=embeddings,
        collection_name="resume_data",
        persist_directory="./vector_db"
    )
    


def ingest_data():
        chunks = process_pdf()
        vectors.add_documents(chunks)
        return "Data Ingestion completed"
        


if __name__ == "__main__":
    #  chunks = process_pdf()
    #  print("Total Chunks = ",len(chunks))
    #  for chunk in chunks:
    #     print(chunk)
    #     print("==" * 10)
    #  print(len(docs))
    #  print(docs[0].content)
     print(ingest_data())
    