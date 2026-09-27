import shutil
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

from loaders import load_local_documents, load_websites

from config import (
    MISTRAL_API_KEY,
    CHROMA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


def build_database(urls=None):
    """
    Builds/Rebuilds the Chroma Vector Database.

    Parameters
    ----------
    urls : list
        Optional list of website URLs.
    """

    print("Loading local documents...")

    documents = load_local_documents()

    # Load websites if provided
    if urls:
        print("Loading websites...")
        documents.extend(load_websites(urls))

    if len(documents) == 0:
        print("No documents found.")
        return False

    print(f"Loaded {len(documents)} documents.")

    # -------------------------
    # Split Documents
    # -------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Generated {len(chunks)} chunks.")

    # -------------------------
    # Embeddings
    # -------------------------

    embedding_model = MistralAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY
    )

    # -------------------------
    # Delete Old Database
    # -------------------------

    if os.path.exists(CHROMA_PATH):
      shutil.rmtree(CHROMA_PATH, ignore_errors=True)

    # -------------------------
    # Create Database
    # -------------------------

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )

    print("Database created successfully.")

    return True


# -------------------------
# Run directly
# -------------------------

if __name__ == "__main__":

    build_database()