import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load artifacts
BOOKS_PATH = "artifacts/books_metadata.csv"

# Load data and model once
books = pd.read_csv(BOOKS_PATH)

# Handle missing values in 'text' column if any
books["text"] = books["text"].fillna("")

# Initialize and fit TF-IDF Vectorizer on the fly
# This ensures no version mismatch issues and removes dependence on tfidf.pkl
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books["text"])

def get_trending(top_n=10):
    return books.sort_values(
        ["rating_count", "avg_rating"],
        ascending=False
    ).head(top_n)

def get_book_titles():
    return list(books["title"].values)

def recommend_by_title(book_title, top_n=10):
    if book_title not in books["title"].values:
        return None

    idx = books.index[books["title"] == book_title][0]
    
    # Get the vector for the selected book
    book_vector = tfidf_matrix[idx]
    
    # Compute cosine similarity between this book and all others
    # linear_kernel is equivalent to cosine_similarity for normalized vectors (which TF-IDF are)
    # flattened to get a 1D array
    cosine_sim = linear_kernel(book_vector, tfidf_matrix).flatten()

    # Get pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim))
    
    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the top n similar books (skipping the first one which is the book itself)
    sim_scores = sim_scores[1:top_n+1]
    
    # Get the book indices
    book_indices = [i[0] for i in sim_scores]
    
    # Return the top n most similar books
    recs = books.iloc[book_indices].copy()
    
    # Optional: Sort recommendations by popularity if desired, or keep by similarity
    # recs = recs.sort_values("popularity_score", ascending=False)
    
    return recs[["title", "author", "avg_rating", "rating_count"]]
