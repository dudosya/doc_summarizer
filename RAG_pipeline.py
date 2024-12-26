from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json

def setup_rag_pipeline(corpus_path="corpus/metadata.json"):
    # Load the corpus
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus_data = json.load(f)
    
    # Extract text content from documents
    documents = []
    for doc in corpus_data['documents']:
        # Combine title and content with clear separation
        full_text = f"Title: {doc['title']}\n\nContent:\n{doc['content']}"
        documents.append(full_text)
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.create_documents(documents)
    
    # Create embeddings (using a lightweight model)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store
    vectorstore.save_local("faiss_index")
    
    return vectorstore

def query_documents(query, vectorstore, k=3):
    """
    Query the vector store for similar documents
    """
    docs = vectorstore.similarity_search(query, k=k)
    return docs


