import os
import csv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
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



def query_document(document_text, user_query):
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.chat_models import ChatOpenAI
    from langchain.text_splitter import CharacterTextSplitter

    api_key = os.getenv("OPENAI_API_KEY", "key") 

    # Step 1: Split the document into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,  # Focused chunks for precise matching
        chunk_overlap=100
    )
    texts = text_splitter.split_text(document_text)

    # Step 2: Embed the document chunks
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Step 3: Retrieve the most relevant chunks for the query
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Top 3 chunks for relevance
    relevant_docs = retriever.get_relevant_documents(user_query)

    # Combine relevant chunks into a single text
    relevant_text = " ".join([doc.page_content for doc in relevant_docs])

    # Step 4: Generate the answer based on the relevant text
    chat_model = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=api_key,
    )

    prompt_template = """
    You are an AI assistant answering questions based strictly on the provided context.

    Context:
    {context}

    Question:
    {query}

    Provide a concise and accurate answer based only on the context above.
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "query"]
    )

    llm_chain = LLMChain(llm=chat_model, prompt=prompt)

    # Generate the answer
    answer = llm_chain.run(context=relevant_text, query=user_query)

    # Log the results to a file
    log_qa_to_file(user_query, answer, relevant_text)

    # Return the generated answer and relevant text
    return answer.strip(), relevant_text.strip()
