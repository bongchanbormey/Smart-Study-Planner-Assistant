import pandas as pd

def clean_books_dataset(input_file, output_file):
    try:
        # Load the dataset with error handling
        books = pd.read_csv(input_file, on_bad_lines="skip")
        print("Dataset loaded successfully.")
        
        # Define the expected columns
        expected_columns = ["bookID", "title", "authors", "average_rating", "isbn",
                            "isbn13", "language_code", "num_pages", "ratings_count",
                            "text_reviews_count", "publication_date", "publisher"]
        
        # Find intersection of actual and expected columns
        actual_columns = [col for col in expected_columns if col in books.columns]
        if not actual_columns:
            raise ValueError("No matching columns found in the dataset.")
        
        # Keep only the relevant columns
        books = books[actual_columns]
        
        # Drop rows with missing or invalid data
        books.dropna(inplace=True)
        
        # Convert numeric columns to appropriate data types (if present)
        numeric_columns = ["average_rating", "num_pages", "ratings_count", "text_reviews_count"]
        for col in numeric_columns:
            if col in books.columns:
                books[col] = pd.to_numeric(books[col], errors="coerce")
        
        # Drop rows with NaN values introduced by type conversion
        books.dropna(inplace=True)
        
        # Save the cleaned dataset
        books.to_csv(output_file, index=False)
        print(f"Cleaned dataset saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
input_file = "books.csv"
output_file = "cleaned_books.csv"

# Run the cleaning function
clean_books_dataset(input_file, output_file)
