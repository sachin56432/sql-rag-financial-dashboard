# SQL + RAG Financial Dashboard

An interactive financial analytics dashboard that combines **MySQL, SQL queries, Retrieval-Augmented Generation (RAG), and a local Large Language Model (LLM)** to analyze financial transactions and answer questions about financial records and supporting notes.

## Features

- **Financial KPIs:** Displays total revenue, total expenses, and net profit.
- **Monthly Analytics:** Visualizes monthly revenue and expenses using interactive Plotly charts.
- **SQL Integration:** Retrieves and aggregates transaction data from MySQL.
- **RAG-Based Question Answering:** Retrieves relevant financial notes from a ChromaDB vector database.
- **Local LLM:** Uses TinyLlama to generate natural-language answers without requiring a paid inference API.
- **Interactive Chatbot:** Allows users to ask questions about financial performance through Streamlit.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend and dashboard | Streamlit |
| Database | MySQL |
| Data processing | Python, Pandas |
| Data visualization | Plotly |
| LLM | TinyLlama 1.1B Chat |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector database | ChromaDB |
| LLM framework | LangChain |

## Project Structure

```text
RAG+SQL/
├── dashboard.py
├── db_connection.py
├── rag_chat.py
├── rag_ingest.py
├── vector_store.py
├── docs/
│   └── expense_notes.txt
├── chroma_db/             # Generated locally; not committed
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. **Data storage:** Financial transactions are stored in a MySQL database.
2. **SQL analytics:** SQL queries calculate monthly revenue, expenses, and net profit.
3. **Document ingestion:** Financial notes are loaded and split into smaller text chunks.
4. **Embedding generation:** Sentence Transformers converts document chunks into vector embeddings.
5. **Vector retrieval:** ChromaDB retrieves relevant notes based on the user's question.
6. **Answer generation:** TinyLlama uses the SQL results, retrieved notes, and question to generate a natural-language response.
7. **Dashboard display:** Streamlit presents financial KPIs, charts, transaction summaries, and chatbot answers.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/sql-rag-financial-dashboard.git
cd sql-rag-financial-dashboard
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database and a `transactions` table with the following columns:

- `id`
- `transaction_date`
- `category`
- `transaction_type`
- `amount`

Insert your financial transaction records and configure `db_connection.py` with the appropriate database connection settings.

**Security:** Store database credentials in environment variables or a local `.env` file. Never commit passwords, API tokens, or private financial data.

### 5. Prepare the RAG Documents

Place your financial notes inside the `docs/` directory.

Run the ingestion script if your project uses it to prepare the document embeddings and vector store:

```bash
python rag_ingest.py
```

Follow any additional setup required by your `vector_store.py` implementation.

### 6. Run the Dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

The first run may download the language model and embedding model, requiring additional disk space and internet access.

## Example Questions

- What are the total revenues and expenses?
- Compare revenue in August and September.
- What expenses were recorded in August?
- Why did salary expenses increase in September?

The SQL database supplies financial figures, while the RAG component retrieves relevant supporting notes. Explanations should only be provided when supported by documented information.

## Important Limitations

- Answers depend on the accuracy and completeness of the database and financial notes.
- Small local language models can make arithmetic or reasoning mistakes. Use SQL or Python for reliable financial calculations.
- The project is a demonstration and should not be used as a substitute for professional accounting or financial advice.
- Database records, credentials, and generated model files should be managed securely.

## Future Improvements

- Add date-range and category filters.
- Include transaction-level search.
- Improve numerical question routing using SQL.
- Add financial trend analysis and expense alerts.
- Improve chatbot answer validation and error handling.
- Add automated tests and deployment support.

## License

Add a license file if you intend to distribute the project publicly. Until then, all rights are reserved by the copyright holder.
