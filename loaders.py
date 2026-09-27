import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    WebBaseLoader
)

from config import UPLOAD_FOLDER


def load_local_documents():
    """
    Load all PDF, TXT and DOCX files
    from the uploads folder.
    """

    documents = []

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    for file in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(UPLOAD_FOLDER, file)

        try:

            # -----------------------
            # PDF
            # -----------------------

            if file.lower().endswith(".pdf"):

                loader = PyPDFLoader(path)

                documents.extend(loader.load())

            # -----------------------
            # TXT
            # -----------------------

            elif file.lower().endswith(".txt"):

                loader = TextLoader(
                    path,
                    encoding="utf-8"
                )

                documents.extend(loader.load())

            # -----------------------
            # DOCX
            # -----------------------

            elif file.lower().endswith(".docx"):

                loader = Docx2txtLoader(path)

                documents.extend(loader.load())

        except Exception as e:

            print(f"Error loading {file}")

            print(e)

    return documents


def load_websites(urls):
    """
    Load website data.

    urls should be a list.

    Example:

    [
        "https://nit.ac.in",
        "https://langchain.com"
    ]
    """

    documents = []

    try:

        loader = WebBaseLoader(urls)

        documents.extend(loader.load())

    except Exception as e:

        print("Website Loading Error")

        print(e)

    return documents