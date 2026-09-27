import os
import shutil
import streamlit as st

from build_db import build_database
from config import UPLOAD_FOLDER
from rag import ask_question

# ===============================
# Page Configuration
# ===============================

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# Create Upload Folder
# ===============================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===============================
# Session State
# ===============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# Sidebar
# ===============================

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.success("Mistral + LangChain + ChromaDB")

    st.divider()

    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF / TXT / DOCX",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for file in uploaded_files:

            save_path = os.path.join(
                UPLOAD_FOLDER,
                file.name
            )

            with open(save_path, "wb") as f:
                f.write(file.getbuffer())

        st.success("Files Uploaded Successfully!")

    st.divider()

    st.subheader("🌐 Website")

    website = st.text_input(
        "Website URL"
    )

    st.divider()

    if st.button("🔄 Build Database"):

        with st.spinner("Building Database..."):

            urls = []

            if website.strip():
                urls.append(website.strip())

            build_database(urls)

        st.success("Database Built Successfully!")

    st.divider()

    st.subheader("🗂 Uploaded Files")

    files = os.listdir(UPLOAD_FOLDER)

    if files:

        for file in files:

            col1, col2 = st.columns([4,1])

            with col1:
                st.write(f"📄 {file}")

            with col2:

                if st.button(
                    "❌",
                    key=file
                ):

                    os.remove(
                        os.path.join(
                            UPLOAD_FOLDER,
                            file
                        )
                    )

                    st.rerun()

    else:

        st.info("No uploaded files.")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ===============================
# Main Page
# ===============================

st.title("📚 AI Knowledge Assistant")

st.caption(
    "Chat with your PDFs, DOCX, TXT files and websites."
)

# ===============================
# Dashboard
# ===============================

files = os.listdir(UPLOAD_FOLDER)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Documents",
    len(files)
)

col2.metric(
    "Vector DB",
    "Ready"
    if os.path.exists("chroma_db")
    else "Not Built"
)

col3.metric(
    "LLM",
    "Mistral"
)

st.divider()

# ===============================
# Display Chat History
# ===============================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ===============================
# Chat Input
# ===============================

question = st.chat_input(
    "Ask a question about your documents..."
)
# ============================================
# Import RAG
# ============================================



# ============================================
# User Chat
# ============================================

if question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate Answer

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer, docs = ask_question(question)

            except Exception as e:

                st.error(e)

                st.stop()

        st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # ============================
        # Retrieved Sources
        # ============================

        with st.expander("📄 Retrieved Sources"):

            if len(docs) == 0:

                st.warning("No source documents found.")

            else:

                for i, doc in enumerate(docs, start=1):

                    st.markdown(f"### 📄 Chunk {i}")

                    source = doc.metadata.get(
                        "source",
                        "Unknown"
                    )

                    st.write(
                        f"**Source:** {source}"
                    )

                    if "page" in doc.metadata:

                        st.write(
                            f"**Page:** {doc.metadata['page'] + 1}"
                        )

                    st.info(doc.page_content)

                    st.divider()