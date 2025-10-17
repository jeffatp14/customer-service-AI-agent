from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from pathlib import Path


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # points to src/
csv_path = BASE_DIR.parent / "transaction_datamart.csv"
df_transaction = pd.read_csv(csv_path)

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_loc = str(Path(__file__).parent / "chrome_langchain_db")
add_documents = not os.path.exists(db_loc)

if add_documents:
    documents = []
    ids = []

    for _, row in df_transaction.iterrows():
        content = (
            f"Transaction ID: {row['transaction_id']}\n"
            f"Customer: {row['customer_name']}\n"
            f"Product: {row['product_name']}\n"
            f"Transaction Amount: {row['transaction_amount']}\n"
            f"Status: {row['transaction_status']}"
        )

        metadata = {
            "product_category": str(row["product_category"]),
            "product_stock": int(row["stock_quantity"]),
            "customer_email": str(row["customer_email"]),
            "transaction_date": str(row["transaction_date"]),
        }

        document = Document(
            page_content=content,
            metadata=metadata,
            id=str(row["transaction_id"]),
        )

        documents.append(document)
        ids.append(str(row["transaction_id"]))

vector_store = Chroma(
    collection_name="lume_and_co",
    persist_directory=db_loc,
    embedding_function=embeddings,
)


if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)


retriever = vector_store.as_retriever(search_kwargs={"k": 2})
