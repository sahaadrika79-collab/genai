from langchain_chroma import Chroma
from langchain_mistralai import (
    ChatMistralAI,
    MistralAIEmbeddings
)
from langchain_core.prompts import ChatPromptTemplate

from config import (
    MISTRAL_API_KEY,
    CHROMA_PATH,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K,
    FETCH_K
)

# ==========================
# Embedding Model
# ==========================

embedding_model = MistralAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=MISTRAL_API_KEY
)

# ==========================
# Load Chroma
# ==========================

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

# ==========================
# Retriever
# ==========================

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": TOP_K,
        "fetch_k": FETCH_K
    }
)

# ==========================
# LLM
# ==========================

llm = ChatMistralAI(
    model=LLM_MODEL,
    api_key=MISTRAL_API_KEY,
    temperature=0
)

# ==========================
# Prompt
# ==========================

PROMPT = """
You are an AI assistant.

Answer ONLY using the supplied context.

If the answer is not available in the context,
reply with:

"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(PROMPT)

# ==========================
# Ask Function
# ==========================

def ask_question(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    final_prompt = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(final_prompt)

    return response.content, docs


# ==========================
# Testing
# ==========================

if __name__ == "__main__":

    question = input("Ask: ")

    answer, docs = ask_question(question)

    print("\nANSWER\n")

    print(answer)

    print("\nSOURCES\n")

    for doc in docs:

        print(doc.metadata)