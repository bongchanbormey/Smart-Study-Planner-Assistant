import openai
import streamlit as st
from PyPDF2 import PdfReader
import re

# Set OpenAI API key
openai.api_key = "ADD-YOUR-OPENAI-API-KEY-HERE"

# Extract text from a PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text()
    return raw_text

# Clean and format text
def clean_text(raw_text):
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

# GPT-3.5 Turbo Summarizer function using chat-based model
def summarize_with_gpt35(text, summary_length):
    # Set the prompt to summarize the text
    prompt = f"Summarize the following document:\n\n{text}"

    # Adjust the max tokens based on desired summary length
    max_tokens_mapping = {
        "Short": 150,   # ~120-150 words
        "Medium": 250,  # ~200-250 words
        "Long": 350     # ~300-350 words
    }
    max_tokens = max_tokens_mapping.get(summary_length, 250)

    # Prepare the messages for the chat model
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes text."},
        {"role": "user", "content": prompt}
    ]

    # Request completion from OpenAI API using GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.5,  # Lower temperature for more focused responses
        n=1,              # We only want one response
        stop=None         # No stop sequence
    )

    # Return the summary text
    return response.choices[0].message['content'].strip()

# Streamlit UI
def document_summarizer_ui():
    # Upload document
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

    if uploaded_file:
        raw_text = extract_text_from_pdf(uploaded_file)
        cleaned_text = clean_text(raw_text)

        # Display extracted text
        st.subheader("Extracted Document Text")
        st.text_area("Document Content", cleaned_text, height=300)

        # Summarization options
        st.subheader("Summary Options")
        summary_length = st.selectbox("Choose summary length", ["Short", "Medium", "Long"])

        # Generate summary using GPT-3.5 Turbo
        if st.button("Summarize Document"):
            with st.spinner("Generating summary..."):
                summary = summarize_with_gpt35(cleaned_text, summary_length)
                st.subheader("Generated Summary")
                st.write(summary)
