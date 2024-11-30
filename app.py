import streamlit as st
from PyPDF2 import PdfReader
from document_qa import query_document
import re
import pandas as pd
import os

# Helper function to clean and format PDF text
def clean_pdf_text(raw_text):
    """
    Cleans and formats raw text extracted from a PDF document.
    - Removes extra newlines.
    - Combines lines into complete sentences where possible.
    """
    text = re.sub(r'\n+', '\n', raw_text)
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():
            # Merge incomplete lines with previous line
            if cleaned_lines and not line.endswith(('.', '!', '?')):
                cleaned_lines[-1] += " " + line.strip()
            else:
                cleaned_lines.append(line.strip())
    formatted_text = "\n\n".join(cleaned_lines)
    return formatted_text

# Streamlit app configuration
st.set_page_config(page_title="Smart Study Planner", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = "Home"

# Sidebar options
options = ["Home", "Document Q&A", "Study Planner"]
selected_option = st.sidebar.radio("Go to", options)
st.session_state.selected_option = selected_option

# Main content layout
if st.session_state.selected_option == "Home":
    st.title("Welcome to the Smart Study Planner")
    st.write("""
        ### Home Page
        This is your smart study assistant that will help you plan and organize your study sessions.
        
        ### How to Use:
        - **Document Q&A**: Upload a document and ask questions to extract relevant information.
        - **Study Planner**: Plan your study sessions and set goals.
    """)

elif st.session_state.selected_option == "Document Q&A":
    st.title("📄 Document Question and Answer")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        # Extract text from uploaded PDF
        reader = PdfReader(uploaded_file)
        raw_text = "".join(page.extract_text() for page in reader.pages)

        # Clean and format the extracted text
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
                st.markdown(relevant_text)  # Using `st.markdown()` to properly render bold text in markdown format

            except Exception as e:
                st.error(f"An error occurred while processing your query: {str(e)}")
        
        # Display Q&A history from the CSV file
        if os.path.exists('qa_log.csv'):
            qa_df = pd.read_csv('qa_log.csv')
            st.subheader("Q&A History")
            st.dataframe(qa_df)

elif st.session_state.selected_option == "Study Planner":
    st.title("📅 Study Planner")
    st.write("This feature is under development!")
