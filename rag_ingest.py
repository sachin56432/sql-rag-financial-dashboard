
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the financial notes
loader = TextLoader(
    "expense_notes.txt",
    encoding="utf-8"
)

documents = loader.load()

# Split the document into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Total documents loaded:", len(documents))
print("Total chunks created:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk.page_content)
