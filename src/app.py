import streamlit as st
from PyPDF2 import PdfReader
import io
import os
from dotenv import load_dotenv

from agent import StudyNotesAgent  # Changed from src.agent

# --- Page Configuration ---
st.set_page_config(
    page_title="Study Notes Summarizer & Quiz Generator",
    page_icon="📚",
    layout="wide",
)

# --- Load Environment Variables and API Key Check ---
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def api_key_check():
    if not GEMINI_API_KEY:
        st.error("🚨 GEMINI_API_KEY is not set! Please add it to your .env file.")
        st.stop()

api_key_check()

# --- PDF Processing ---
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# --- Main App ---
st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload your study notes in PDF format, and let the agent summarize them and generate a quiz for you!")

# --- Sidebar for PDF Upload ---
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
        st.success("PDF uploaded successfully!")

# --- Main Content Area ---
if uploaded_file:
    # Initialize the agent only if a file is uploaded
    agent = StudyNotesAgent()

    # Extract and store text
    pdf_text = extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    if pdf_text:
        st.session_state['pdf_text'] = pdf_text

        col1, col2 = st.columns(2)

        with col1:
            st.header("📄 Extracted Text")
            st.text_area("Full text from PDF", pdf_text, height=300)

        with col2:
            st.header("🤖 Agent Actions")
            
            if st.button("Generate Summary", use_container_width=True):
                if 'pdf_text' in st.session_state and st.session_state['pdf_text']:
                    with st.spinner("Generating summary..."):
                        summary = agent.generate_summary(st.session_state['pdf_text'])
                    st.subheader("📝 Summary")
                    st.write(summary)
                else:
                    st.warning("Please upload a PDF first.")
            
            if st.button("Create Quiz", use_container_width=True):
                if 'pdf_text' in st.session_state and st.session_state['pdf_text']:
                    with st.spinner("Generating quiz..."):
                        quiz = agent.generate_quiz(st.session_state['pdf_text'])
                    st.subheader("❓ Quiz")
                    st.markdown(quiz)
                else:
                    st.warning("Please upload a PDF first.")
else:
    st.info("Please upload a PDF file in the sidebar to get started.")