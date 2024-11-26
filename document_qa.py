import openai
import PyPDF2
import os
import csv

# Set up OpenAI API key
openai.api_key = "key"

# Log questions and answers into a CSV file
def log_qa_to_file(question, answer, relevant_text):
    file_exists = os.path.exists('qa_log.csv')
    with open('qa_log.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header if the file is empty
        if not file_exists:
            writer.writerow(["Question", "Answer", "Relevant Text"])
        writer.writerow([question, answer, relevant_text])

# Function to query document using OpenAI's GPT model
def query_document(document_text, user_query):
    prompt = f"Document: {document_text}\n\nQuestion: {user_query}\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or use any model of your choice
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
    )

    answer = response['choices'][0]['message']['content']
    
    # Save the question, answer, and relevant text to a log file
    relevant_text = answer  
    
    log_qa_to_file(user_query, answer, relevant_text)
    
    return answer, relevant_text
