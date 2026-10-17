
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="financial_notes",
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

question = "Why did salary expenses increase in September?"

results = vector_store.similarity_search(question, k=2)

for doc in results:
    print("\nRetrieved document:")
    print(doc.page_content)
