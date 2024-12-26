# from RAG_pipeline import setup_rag_pipeline, query_documents

# vectorstore = setup_rag_pipeline()
# query = "встатье 16:впункте 1:подпункт 9-3)изложить в следующей редакции:\"9-3) обсуждает вопрос о передаче"
# relevant_docs = query_documents(query, vectorstore)


# Load the saved vector store
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize the same embeddings model you used to create the index
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load the saved index
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Now you can query it
query = "Что ты думаешь об этом тексте?"  # replace with your question
relevant_docs = vectorstore.similarity_search(query, k=3)  # get top 3 most relevant chunks

# Print the retrieved documents
for i, doc in enumerate(relevant_docs, 1):
    print(f"\nDocument {i}:")
    print(doc.page_content)