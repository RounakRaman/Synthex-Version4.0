import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page config
st.set_page_config(page_title="SyntheX", page_icon="🔍", layout="wide")

# Custom CSS to style the app with a light purplish background and white title
st.markdown("""
    <style>
        /* Set background color to a light purple and text color to dark purple */
        .reportview-container {
            background-color: #A100FF; /* Light purple */
            color: #A100FF;  /* Dark purple */
        }

        /* Set headers to white */
        h1, h2, h3, h4, h5, h6 {
            color: white;
        }

        /* Style sidebar with a darker purple */
        .sidebar .sidebar-content {
            background-color: #A100FF;
        }

        /* Style the submit button */
        .stButton>button {
            background-color: #A100FF;
            color: white;
            border-radius: 10px;
        }

        /* Style the spinner during processing */
        .stSpinner {
            color: #4B0082;
        }

        /* Customize text input box */
        .stTextInput>div>input {
            background-color: #A100FF;
            color: #A100FF;
            border-radius: 5px;
        }

        /* Style file uploader */
        .stFileUploader {
            color: #4B0082;
        }
    </style>
""", unsafe_allow_html=True)


# Function to extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vector store for document search
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to load the conversational chain for question answering
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context and think from a business perspective. 
    You can take hints from open-source information or Google but stick to the document part only. 
    If the answer is not in the provided in context, just say, "answer is not available in the context".
    
    Context:\n {context}\n
    Question:\n {question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input and generate response
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    # Display the response in the app
    st.write("**Reply**: ", response["output_text"])

# Main function to run the app
def main():
    st.title("💡 SyntheX - Unlocking Insights from Text, Video & Audio")
    col1, col2 = st.columns(2)

# Add content to the first column
    with col1:
        st.page_link("pages/synthex_MeetSnaps.py",label="SyntheX MeetSnaps",icon="🎥")
    

# Add content to the second column
    with col2:
        st.page_link("pages/synthex_TalkTrack.py",label="SyntheX TalkTrack",icon="🎤")
    

    
    
    # User input for question
    user_question = st.text_input(" Ask any Question from the PDF/Internal Documents: ❓")

    # Display user question response
    if user_question:
        user_input(user_question)

    # Sidebar for PDF upload
    with st.sidebar:
        
        st.header("📂 Upload Documents:")
        pdf_docs = st.file_uploader("Upload your PDF Files/Documents", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Documents Processed Successfully!")

# Run the app
if __name__ == "__main__":
    main()
