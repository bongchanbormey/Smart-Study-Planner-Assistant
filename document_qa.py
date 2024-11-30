import os
import csv
import re
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# Log questions and answers into a CSV file
def log_qa_to_file(question, answer, relevant_text):
    file_exists = os.path.exists('qa_log.csv')
    with open('qa_log.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Question", "Answer", "Relevant Text"])
        writer.writerow([question, answer, relevant_text])

# Extract relevant sentences from the document
def extract_relevant_text(document_text, user_query):
    keyword = re.escape(user_query.lower())  # Escape special characters in the query
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', document_text)  # Split into sentences

    # Extract sentences that contain the keyword
    relevant_sentences = [sentence for sentence in sentences if re.search(r'\b' + keyword + r'\b', sentence.lower())]

    # Highlight the keyword within the relevant sentences
    highlighted_sentences = [
        re.sub(r'\b' + keyword + r'\b', lambda match: f"**{match.group(0)}**", sentence, flags=re.IGNORECASE)
        for sentence in relevant_sentences
    ]

    # Join all relevant sentences into a single text block
    return " ".join(highlighted_sentences)

# Query the document and return the answer and relevant text
def query_document(document_text, user_query):
    api_key = os.getenv("OPENAI_API_KEY", "key")
    # Step 1: Split the document into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,  # Split into focused chunks
        chunk_overlap=100
    )
    texts = text_splitter.split_text(document_text)

    # Step 2: Embed the document chunks
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Step 3: Retrieve the most relevant chunks for the query
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.get_relevant_documents(user_query)

    # Combine relevant chunks into a single text
    relevant_text_from_docs = " ".join([doc.page_content for doc in relevant_docs])

    # Step 4: Extract relevant text with highlighted keywords
    highlighted_relevant_text = extract_relevant_text(relevant_text_from_docs, user_query)

    # Step 5: Generate an answer based on the highlighted relevant text
    chat_model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=api_key,
    )

    prompt_template = """
    You are a helpful AI assistant answering questions based on the provided context. 
    Context:
    {context}

    Question:
    {query}

    Provide a concise, accurate, and detailed answer based on the context above.
    """
    prompt = prompt_template.format(context=relevant_text_from_docs, query=user_query)

    # Generate the answer using the LLM
    answer = chat_model.predict(prompt)

    # Log the results
    log_qa_to_file(user_query, answer, relevant_text_from_docs)

    # Return the answer and the relevant text
    return answer.strip(), relevant_text_from_docs.strip()
