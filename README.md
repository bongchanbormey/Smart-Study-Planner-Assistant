## Smart Study Assistant
### Overview
The Smart Study Planner is part of my final project for COSC 221 - 001: Computer Science B course, taught by Professor Abdallah Altrad. It is a study productivity tool built using Python and Streamlit that is designed to enhance learning and study efficiency. This application provides several useful features, including:

1. Document Q&A
2. Study Planner
3. Focus Timer
4. Book Recommender
5. Document Summarizer
  
### Main Features
- Document Q&A: Upload documents and ask questions to extract relevant information.
- Study Planner: Plan and organize your study sessions.
- Focus Timer: Stay focused with customizable study sessions.
- Book Recommender: Discover book recommendations based on your interests.
- Document Summarizer: Generate concise summaries of uploaded documents.


### 1. **Document Q&A** (`document_qa.py`)
This tool allows users to upload a PDF document and interact with it by asking questions. Using a combination of **OpenAI's GPT-3.5 Turbo** and document parsing, this module provides users with relevant answers from the content of the uploaded document.

- **Features:**
  - Upload a PDF document.
  - Extract and clean text from the document.
  - Ask questions related to the document and receive answers based on the content.

- **Dependencies:**
  - `openai`: For GPT-3.5 Turbo API (you may need to sign up for an openai account and generate an OpenAI API key).
  - `PyPDF2`: For PDF text extraction.

---

### 2. **Study Planner** (`study_planner.py`)
This tool helps users organize their study sessions by creating a personalized study schedule based on the subject, priority level, and available study time as well as keeping track of the progress of those tasks.

- **Features:**
  - Create a study schedule based on user input (subject, priority level, time).
  - Tracks progress.
  - Display monthly calendar.

- **Dependencies:**
  - `streamlit`: For the web app interface (streamlit_calendar library for monthly calendar display)

---

### 3. **Focus Timer** (`focus_timer.py`)
This timer helps users maintain focus by creating work-break cycles (e.g., Pomodoro Technique). It lets users customize work durations, break durations, and total number of sessions.

- **Features:**
  - Set custom focus durations (in minutes).
  - Set focus, short, and long break durations.
  - Track the number of sessions completed.
  - Visual display of the current timer, including remaining time for focus or break periods.

- **Dependencies:**
  - `streamlit`: For the web interface.
  - `time`: For handling timer functionality.

---

### 4. **Book Recommender** (`books.py`)
This tool helps users discover books based on a specific book title. It utilizes **cosine similarity** between book features (such as authors, publishers, language, etc.) to recommend books similar to the user's input. It is based on a dataset named "Goodreads-books) retrieved from Kaggle (https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks?resource=download) which has about 45K books listed.

- **Features:**
  - Input a book title, author, genre, or publisher, and the app suggests 5 similar books.
  - Recommends books based on author, publisher, and language.
  - Displays book details such as title, authors, average rating, and publisher.

- **Dependencies:**
  - `streamlit`: For the web app interface.
  - `pandas`: For data manipulation.
  - `sklearn`: For calculating cosine similarity.

---

### 5. **Document Summarizer** (`summarizer.py`)
This tool allows users to upload a PDF document, clean and extract the text, and generate a summary using **OpenAI's GPT-3.5 Turbo**. Users can select the length of the summary (short, medium, or long).

- **Features:**
  - Upload and extract text from a PDF.
  - Clean and format the extracted text for better readability.
  - Generate a summary using GPT-3.5 Turbo based on user-specified summary length.

- **Dependencies:**
  - `openai`: For GPT-3.5 Turbo API (you may need to sign up for an openai account and generate an OpenAI API key).
  - `PyPDF2`: For PDF text extraction.
  - `re`: For text formatting and cleaning.
  - `streamlit`: For the web app interface.

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

### **2. Install Required Dependencies**
The project requires the following Python libraries:
- `streamlit`
- `openai`
- `pandas`
- `sklearn`
- `PyPDF2`

To install them, run:

```bash
pip install -r requirements.txt
```

Alternatively, install the dependencies manually:

```bash
pip install streamlit openai pandas scikit-learn PyPDF2
```

P.S. Use 'pip3' depending on the version that you've installed.

### **3. Set up OpenAI API Key**
For the **Document Q&A** and **Document Summarizer** tools, you need to set up your OpenAI API key.

1. Sign up for OpenAI and get your API key [here](https://openai.com/index/openai-api/).
2. Replace the `"add-your-openai-api-key-here"` placeholder in the code with your actual API key.

---

## **Running the Application**

Once the dependencies are installed and the OpenAI API key is set up, you can run the Streamlit app by executing the following command in your terminal:

```bash
streamlit run <script-name>.py
```

For example, to run the **Focus Timer**:

```bash
streamlit run focus_timer.py
```

This will start a local server and open the web app in your default browser.

---

## **How to Use Each Tool**

### **Document Q&A**
1. Upload a PDF document.
2. Ask any questions related to the content of the document.
3. Receive a direct answer from the model based on the document content.

### **Study Planner**
1. Enter your study subjects, priority, and available time for each session.
2. View your personalized study schedule/calendar.
3. Track progress.

### **Focus Timer**
1. Set your work session time, short break duration, and long break time.
2. Start the timer and stay focused during work sessions.
3. Track your session progress and take breaks as scheduled.

### **Book Recommender**
1. Type a book title, author, or genre you are interested in.
2. Receive recommendations based on books that match your input.
3. View details about the recommended books, including authors, ratings, and publishers.

### **Document Summarizer**
1. Upload a PDF document.
2. Choose the desired summary length (short, medium, or long).
3. Receive a summarized version of the document.

---
