import streamlit as st
from PyPDF2 import PdfReader
from document_qa import query_document
import re
import pandas as pd
import os
from study_planner import study_planner_ui
from focus_timer import focus_timer
from books import book_recommendation_ui
from summarizer import document_summarizer_ui

# Streamlit app configuration - must be the first command
st.set_page_config(page_title="Smart Study Planner", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = "Home"

# Sidebar options
options = ["Home", 
           "Document Q&A", 
           "Study Planner", 
           "Focus Timer", 
           "Book Recommender",
           "Document Summarizer"]
selected_option = st.sidebar.radio("Go to", options)
st.session_state.selected_option = selected_option

# Helper function to clean and format PDF text
def clean_pdf_text(raw_text):
    text = re.sub(r'\n+', '\n', raw_text)
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():
            if cleaned_lines and not line.endswith(('.', '!', '?')):
                cleaned_lines[-1] += " " + line.strip()
            else:
                cleaned_lines.append(line.strip())
    formatted_text = "\n\n".join(cleaned_lines)
    return formatted_text

# Helper function to display the header image
def display_header_image(page_name):
    # Map page names to corresponding image filenames
    header_images = {
        "Home": "1-home.png",
        "Document Q&A": "2-doc-qa.png",
        "Study Planner": "4-study-planner.png",
        "Focus Timer": "5-timer.png",
        "Book Recommender": "6-book.png",
        "Document Summarizer": "3-summarizer.png"
    }
    
    # Get the image path for the selected page
    header_image_path = header_images.get(page_name, "1-home.png")  # Default to Home image if not found
    st.image(header_image_path, use_container_width=True)

# Main content layout
if st.session_state.selected_option == "Home":
    display_header_image("Home")
    st.title("Welcome to the Smart Study Planner")
    st.write("""
        ### Home Page
        This is your smart study assistant that will help you plan and organize your study sessions.
        
        ### How to Use:
        - **Document Q&A**: Upload a document and ask questions to extract relevant information.
        - **Study Planner**: Plan your study sessions and set goals.
        - **Focus Timer**: Set time for your study sessions for better focus.
        - **Book Recommendation**: Find more books of your interest to read.
        - **Document Summarizer**: Get a summary of your document.
    """)

elif st.session_state.selected_option == "Document Q&A":
    display_header_image("Document Q&A")
    st.title("📄 Document Question and Answer")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()

        # Clean and format extracted text
        cleaned_text = clean_pdf_text(raw_text)
        st.text_area("Document Content", cleaned_text, height=300)

        # User input for question
        user_query = st.text_input("Ask a Question about the document:")

        if user_query:
            try:
                # Get answer using LangChain
                with st.spinner("Processing your query..."):
                    answer, relevant_text = query_document(cleaned_text, user_query)
                
                # Display the result
                st.subheader("Answer:")
                st.write(f"**Question:** {user_query}")
                st.write(f"**Answer:** {answer}")

                # Render relevant text with markdown to properly display bold keywords
                st.subheader("Relevant Text from Document:")
                st.markdown(relevant_text)  

            except Exception as e:
                st.error(f"An error occurred while processing your query: {str(e)}")
        
        # Display Q&A history from the CSV file
        if os.path.exists('qa_log.csv'):
            qa_df = pd.read_csv('qa_log.csv')
            st.subheader("Q&A History")
            st.dataframe(qa_df)

elif st.session_state.selected_option == "Study Planner":
    display_header_image("Study Planner")
    st.title("📅 Study Planner")
    study_planner_ui()

elif st.session_state.selected_option == "Focus Timer":
    display_header_image("Focus Timer")
    st.title("⏳ Focus Timer")
    focus_timer()

elif st.session_state.selected_option == "Book Recommender":
    display_header_image("Book Recommender")
    st.title("📚 Book Recommendation")
    book_recommendation_ui()
    
elif st.session_state.selected_option == "Document Summarizer":
    display_header_image("Document Summarizer")
    st.title("📄 Document Summarizer")
    document_summarizer_ui()
