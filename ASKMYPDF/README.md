
# 📚 AskMyPdf Chatbot with Qdrant + Gemini

A simple, context-aware ai chatbot that uses Qdrant for document storage and retrieval, and Gemini (or GPT) for natural language understanding and response generation. The app enables users to upload a PDF, which is then processed and stored in a Qdrant vector store. The chatbot answers questions based on the context from the uploaded PDF.

## 🚀 Features
- Upload PDF files
- Split PDFs into manageable chunks for better search and retrieval
- Use Google Gemini (or OpenAI) model for natural language understanding
- Retrieve relevant document chunks based on user input
- Answer questions using context from the PDF with page references

---

## 🛠 Prerequisites

To run this project, make sure you have the following tools and libraries installed:

- Python 3.7+ (recommended)
- [Qdrant](https://qdrant.tech/) running locally at `http://localhost:6333`
- `.env` file with valid Gemini API key

---

## 🔧 Installation Steps

### 1. Set Up the Virtual Environment

It’s recommended to use a virtual environment for Python dependencies.

### 2. Install Required Libraries

Use `pip` to install the necessary dependencies:

```bash
pip install -r requirements.txt
```
If a Python module is missing and not listed in requirements.txt, install it manually:

```bash
pip install <module_name>
```


### 3. Set Up `.env` File

Create a `.env` file in the root directory and add your **Google Gemini API key** (or OpenAI API key if using OpenAI instead of Gemini):

```
Gemini_API="your-gemini-api-key-here"
```
### 4. Qdrant Docker Compose Setup

This repository contains a qdrant-compose.yaml file to quickly set up and run Qdrant, a vector search engine, using Docker

```
docker-compose -f qdrant-compose.yaml up
```

Make sure Qdrant is running locally at `http://localhost:6333`. You can follow [Qdrant's quickstart guide](https://qdrant.tech/documentation/quickstart/) to get it running.

---

## 🏃‍♂️ Running the App

1. **Start the Streamlit app**:
   
   After installing dependencies and setting up the `.env` file, run the following command:

   ```bash
   streamlit run app.py
   ```

2. **Access the Web Interface**:

   The app will open in your browser. If it doesn't, navigate to `http://localhost:8501` in your browser.

---

## 🧑‍💻 Using the App

1. **Upload a PDF**:
   - In the sidebar, click on the "Upload PDF" button.
   - Choose a PDF file you want to process. The file will be split into chunks for easier search and retrieval.
   
2. **Ask Questions**:
   - After uploading the PDF, you can start typing your questions in the chat input.
   - The assistant will answer based on the context found in the PDF, including relevant page numbers.

---

## ⚠️ Error Handling

The app has built-in error handling for common issues:

- **Missing API Key**: If the Gemini API key is missing or invalid, you’ll see an error message on the UI.
- **PDF Processing Failures**: If the PDF file cannot be processed, the app will display an error.
- **Qdrant Connection Errors**: If there’s an issue connecting to Qdrant, an error message will appear.
- **Model Errors**: If there’s a problem with the model response, an error message will be shown.

---

## 🧑‍💻 Code Overview

The main components of the code are:

1. **PDF Upload & Processing**:
   - The PDF is uploaded and processed using `PyPDFLoader` from LangChain.
   - It is split into smaller chunks using `RecursiveCharacterTextSplitter`.

2. **Vector Storage (Qdrant)**:
   - The document chunks are stored in a Qdrant vector store, where embeddings are used for efficient retrieval.

3. **Embeddings**:
   - The app uses `GoogleGenerativeAIEmbeddings` (or OpenAI) for converting the document text into embeddings.

4. **Chat Interface**:
   - The app uses Streamlit for creating the user interface.
   - It maintains the conversation history using `st.session_state`.

5. **Error Handling**:
   - Errors are caught and displayed in the app using `st.error`.

---

## 💡 Customization

You can customize the app by:
- **Changing the model**: You can switch between `Gemini` and `GPT` models.
- **Adjusting chunk size**: Modify the chunk size in `RecursiveCharacterTextSplitter` to suit your needs.
- **Switching storage backend**: You can replace Qdrant with another vector store if desired.
