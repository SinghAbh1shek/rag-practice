import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variable
load_dotenv()
GOOGLE_API_KEY = os.getenv("Gemini_API")

# Initialize OpenAI client
client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


st.title("AskMyPDF 📚")
st.caption("Upload your PDF and start chatting with it 🔍")

with st.sidebar:
    pdf_file = st.file_uploader("Upload a PDF", type="pdf")

# Process the PDF
if pdf_file:
    # Save PDF locally
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())

    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    # document splitting
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    # Create embeddings
    embedder = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY,
    )

    # Create the collection to Qdrant vector store
    try:
        vector_store = QdrantVectorStore.from_documents(
            documents=split_docs,
            embedding=embedder,
            url="http://localhost:6333",
            collection_name="learning_langchain"
        )
    except Exception as e:
            st.error(f"❌ Error connecting to Qdrant: {e}")
            st.stop()

    st.success("✅ PDF Processed and Added to Qdrant!")

    # Load retriever from existing Qdrant collection
    retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333/",
    collection_name="learning_langchain",
    embedding=embedder
)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Get user input
    if prompt := st.chat_input("Ask something..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Retrieve relevant context
        relevant_docs = retriver.similarity_search(query=prompt)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        system_prompt = f"""
        You are a helpful ai assistant. Your role is to answers questions based on the content of the PDF documents.
        Use only the following context to answer the user's questions.
        If the context doesn't have answers, just reply with "The answer is not available in the provided content."
        If you find the answer the user asked for, include the page number if you can.

        Note:
            - Keep your answer clear and easy to understand.
            - If the user requests a specific number of words for the answer, answer with exactly that number of words.

        Context:
        {context}

        Example: 
        Input: What is Python?
        Output: Python is a high-level, interpreted programming language known for its simplicity and readability. (Page 15)

        Input: What is Python? Answer in 50 words.
        Output: Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data analysis, artificial intelligence, automation, and more. Python’s extensive libraries and community support make it an excellent choice for both beginners and experts. (Page 15)

        Input: Who created Python?
        Output: The answer is not available in the provided content.

        Input: Hey
        Output: I can only answer based on the provided content.

        """

        # Messages to send to model
        messages = [
                { 'role': 'system', 'content': system_prompt },
                {'role': 'user', 'content': prompt}
            ]
        with st.spinner("Thinking..."):
             # Generate response using Gemini model with OpenAI SDK
            response = client.chat.completions.create(
                    # model='gpt-4o-mini',
                    model="gemini-1.5-flash",
                    messages=messages
            )

            answer = response.choices[0].message.content

        st.chat_message("assistant").write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
