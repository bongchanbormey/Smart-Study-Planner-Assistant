import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def load_data():
    try:
        # Load the cleaned dataset
        return pd.read_csv("cleaned_books.csv")
    except FileNotFoundError:
        st.error("Cleaned dataset not found. Please ensure 'cleaned_books.csv' is in the directory.")
        return None

def recommend_books(book_title, books_df):
    try:
        # Combine relevant features
        books_df["features"] = books_df["authors"] + " " + books_df["publisher"] + " " + books_df["language_code"]
        
        # Vectorize features
        vectorizer = CountVectorizer()
        feature_matrix = vectorizer.fit_transform(books_df["features"])
        
        # Compute cosine similarity
        similarity = cosine_similarity(feature_matrix, feature_matrix)
        
        # Find the book index
        book_idx = books_df[books_df["title"].str.contains(book_title, case=False, na=False)].index[0]
        
        # Get similarity scores and sort
        scores = list(enumerate(similarity[book_idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get top 5 recommendations
        top_recommendations = scores[1:6]
        recommended_books = books_df.iloc[[i[0] for i in top_recommendations]]
        return recommended_books[["title", "authors", "average_rating", "publisher"]]
    except IndexError:
        return None

def book_recommendation_ui():
    # Load data
    books_df = load_data()
    if books_df is None:
        return
    
    # User input
    st.subheader("Find Your Next Book to Read!")
    user_input = st.text_input("Enter a book, author, or genre to get recommendations:")
    
    if user_input:
        recommendations = recommend_books(user_input, books_df)
        if recommendations is not None and not recommendations.empty:
            st.write("### Recommended Books")
            st.dataframe(recommendations)
        else:
            st.warning("No recommendations found. Try another book title.")

