# 🤖 GenAI – AI Knowledge Assistant

A document-based Generative AI application that uses **Retrieval-Augmented Generation (RAG)** to answer questions from uploaded documents and website content.

The application provides a Streamlit-based interface where users can upload PDF, TXT, and DOCX files, optionally provide a website URL, build a searchable vector database, and ask questions about the available information.

---

## 📌 Project Overview

This project is an **AI Knowledge Assistant** built using Python, Streamlit, LangChain, Mistral AI, and ChromaDB.

Instead of relying only on the language model's general knowledge, the application retrieves relevant information from the provided documents and uses that information as context when generating an answer.

The application follows a Retrieval-Augmented Generation workflow:

```text
Documents / Website
        ↓
Document Loading
        ↓
Text Splitting
        ↓
Mistral Embeddings
        ↓
ChromaDB Vector Database
        ↓
MMR Retrieval
        ↓
Relevant Context
        ↓
Mistral LLM
        ↓
Generated Answer
```

---

## ✨ Features

* 📄 Upload multiple PDF, TXT, and DOCX files
* 🌐 Load information from website URLs
* 🔄 Build and rebuild the ChromaDB vector database
* 🧩 Split documents into smaller text chunks
* 🧠 Generate embeddings using Mistral AI
* 🔎 Retrieve relevant information using Maximum Marginal Relevance (MMR)
* 💬 Ask questions through a Streamlit chat interface
* 📚 Display retrieved source documents/chunks
* 📑 Display page numbers when available
* 🗂 View uploaded files
* ❌ Remove uploaded files from the interface
* 🗑 Clear the current chat history
* 📊 Dashboard showing document count, vector database status, and LLM information

The Streamlit interface implements document upload, website input, database building, uploaded-file management, and chat functionality.

---

## 🛠️ Technologies Used

| Technology           | Purpose                               |
| -------------------- | ------------------------------------- |
| Python               | Core programming language             |
| Streamlit            | Web-based user interface              |
| LangChain            | RAG and document-processing framework |
| Mistral AI           | Embeddings and language model         |
| ChromaDB             | Vector database                       |
| PyPDF                | PDF document loading                  |
| Docx2txt             | DOCX document loading                 |
| BeautifulSoup / lxml | Web/document processing dependencies  |
| python-dotenv        | Environment variable management       |

The project dependencies include LangChain, LangChain Community, LangChain Mistral, LangChain Chroma, ChromaDB, Mistral/OpenAI packages, document-processing libraries, Streamlit, and supporting utilities.

---

## 🏗️ Project Structure

```text
genai/
│
├── Document_loader/
│   └── Document loading related files
│
├── uploads/
│   └── Cse.pdf
│
├── app.py
├── build_db.py
├── config.py
├── loaders.py
├── main.py
├── rag.py
├── text.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

#### `app.py`

Contains the Streamlit application interface.

It handles:

* File uploads
* Website URL input
* Database-building button
* Uploaded-file display and deletion
* Chat history
* User questions
* Generated answers
* Retrieved source display

The application is configured with the title **AI Knowledge Assistant** and uses a wide Streamlit layout.

#### `build_db.py`

Builds or rebuilds the ChromaDB vector database.

The process is:

1. Load local documents.
2. Load website content if a URL is provided.
3. Split the documents into chunks.
4. Generate Mistral embeddings.
5. Remove the previous Chroma database.
6. Create a new Chroma vector database.

The implementation uses a chunk size of `500` and an overlap of `50`.

#### `config.py`

Contains the application's configuration values, including:

* Mistral API key
* Upload directory
* ChromaDB directory
* Chunk size
* Chunk overlap
* Embedding model
* LLM model
* Retrieval parameters

Current model settings include:

```text
Embedding model: mistral-embed
LLM model: mistral-small-latest
Chunk size: 500
Chunk overlap: 50
Top K: 3
Fetch K: 5
```

These values are defined in the project's configuration.

#### `loaders.py`

Handles loading different types of data.

Supported local document types:

```text
PDF
TXT
DOCX
```

It also supports loading website content through `WebBaseLoader`.

#### `rag.py`

Contains the Retrieval-Augmented Generation pipeline.

It:

1. Loads the Chroma vector database.
2. Creates the Mistral embedding model.
3. Creates an MMR retriever.
4. Retrieves relevant documents.
5. Places the retrieved text into the prompt.
6. Sends the prompt to the Mistral language model.
7. Returns the generated answer and retrieved documents.

The retriever uses MMR with:

```text
k = 3
fetch_k = 5
```

and the LLM is configured with temperature `0`.

#### `requirements.txt`

Contains the Python packages required by the project.

Install them using:

```bash
pip install -r requirements.txt
```

---

# 🔄 Application Workflow

## 1. Upload Documents

The user can upload one or more:

```text
.pdf
.txt
.docx
```

files through the Streamlit interface.

The files are stored in the configured `uploads` directory.

---

## 2. Add a Website

The application also provides a field where the user can enter a website URL.

```text
Website URL
```

If a URL is provided, it is passed to the database-building process.

---

## 3. Build the Vector Database

When **Build Database** is selected, the application:

```text
Load Documents
      ↓
Load Website Content (if provided)
      ↓
Split Documents
      ↓
Generate Embeddings
      ↓
Create ChromaDB
```

The previous Chroma database is removed before a new database is created.

---

## 4. Ask a Question

The user enters a question in the chat interface:

```text
Ask a question about your documents...
```

The question is sent to the RAG pipeline.

---

## 5. Retrieve Relevant Information

The question is used to search the Chroma vector database.

The application uses **MMR (Maximum Marginal Relevance)** retrieval to obtain relevant documents.

---

## 6. Generate the Answer

The retrieved document content is placed into the prompt along with the user's question.

The prompt instructs the model to answer using the supplied context and to respond that the information could not be found if it is unavailable in that context.

The response is generated using the configured Mistral language model.

---

## 7. Display Sources

After generating an answer, the application provides a **Retrieved Sources** section.

For each retrieved chunk, the interface can show:

* Source
* Page number, when available
* Retrieved text

This allows the user to inspect the information retrieved for the answer.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/sahaadrika79-collab
```

Move into the project directory:

```bash
cd genai
```

---

## 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

The application reads the Mistral API key from an environment variable using `python-dotenv`.

The configuration retrieves:

```python
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
```

rather than storing the API key directly in the configuration.

Create a `.env` file in the project root:

```text
MISTRAL_API_KEY=your_mistral_api_key_here
```

### ⚠️ Important

Never commit `.env` to GitHub.

The `.gitignore` file should exclude:

```text
.env
```

Do not share your actual API key publicly.

---

# ▶️ Running the Application

After activating the virtual environment and installing the dependencies, start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local web address in the terminal.

Open that address in your browser.

---

# 🖥️ Using the Application

### Step 1

Start the application:

```bash
streamlit run app.py
```

### Step 2

Upload a PDF, TXT, or DOCX document.

### Step 3

Optionally enter a website URL.

### Step 4

Click:

```text
🔄 Build Database
```

### Step 5

Wait for the vector database to be created.

### Step 6

Ask a question in:

```text
Ask a question about your documents...
```

### Step 7

Review the generated answer and expand **Retrieved Sources** to inspect the retrieved document chunks.

---

# 📄 Sample Data

The repository contains a sample PDF in:

```text
uploads/Cse.pdf
```

This can be used as an example document for testing the document-based question-answering workflow.

---

# 🔒 Security

The project uses environment variables for the Mistral API key.

The following types of files should remain local and should not be committed:

```text
.env
venv/
__pycache__/
chroma_db/
```

The `.gitignore` file is included in the repository to help prevent these files from being uploaded.

---

# 🚀 Future Improvements

Possible improvements to the project include:

* Support for additional document formats
* More advanced document chunking strategies
* Improved retrieval and ranking
* Persistent conversation history
* Authentication and user management
* Better error handling
* Retrieval and answer-quality evaluation
* Additional LLM providers
* Deployment to a cloud platform
* Improved user interface and document management

---

# 🎓 Project Purpose

This project demonstrates the implementation of a practical **Retrieval-Augmented Generation (RAG)** application using modern Generative AI technologies.

It combines:

```text
Document Processing
        +
Vector Embeddings
        +
Vector Search
        +
Information Retrieval
        +
Large Language Model
        =
AI Knowledge Assistant
```

---

## 👩‍💻 Author

**GenAI Project**

Developed as an educational Generative AI project demonstrating document-based question answering with Retrieval-Augmented Generation.
