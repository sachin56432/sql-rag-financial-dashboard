
import os

os.environ["HF_HOME"] = "D:/huggingface_cache"

from langchain_huggingface import (
    HuggingFacePipeline,
    HuggingFaceEmbeddings,
    ChatHuggingFace,
)
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
)

from db_connection import get_monthly_summary


# 1. Load the local TinyLlama model
llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 180,
        "do_sample": False,
        "return_full_text": False,
    },
)

model = ChatHuggingFace(llm=llm)


# 2. Load the local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 3. Connect to the existing ChromaDB
vector_store = Chroma(
    collection_name="financial_notes",
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 2}
)


# 4. Retrieve financial data from MySQL
def get_sql_data(_):
    df = get_monthly_summary()

    if df.empty:
        return "No financial records found."

    return df.to_string(index=False)


# 5. Format retrieved documents
def format_docs(documents):
    return "\n\n".join(
        doc.page_content for doc in documents
    )


# 6. Create the prompt

prompt = ChatPromptTemplate.from_template("""
You are a financial assistant. Answer the user's question directly.

Rules:
1. Use the SQL results for financial figures.
2. Use retrieved notes only for documented explanations.
3. Never output code, scripts, SQL queries, or instructions.
4. Never invent missing information.
5. Keep the answer short and clear.

SQL financial results:
{sql_data}

Retrieved financial notes:
{context}

User question:
{question}

Provide only the financial answer:
""")



# 7. Build the combined SQL + RAG chain
financial_chain = (
    {
        "sql_data": RunnableLambda(get_sql_data),
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)


# 8. Test the chain
if __name__ == "__main__":
    while True:
        question = input(
            "\nAsk a financial question (or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        try:
            answer = financial_chain.invoke(question)

            print("\nFinancial Assistant:")
            print(answer)

        except Exception as e:
            print(f"\nError: {e}")
