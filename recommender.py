import pandas as pd
import numpy as np
import joblib

# Load artifacts
BOOKS_PATH = "artifacts/books_metadata.csv"
TFIDF_PATH = "artifacts/tfidf.pkl"
COSINE_PATH = "artifacts/cosine_sim.npy"

books = pd.read_csv(BOOKS_PATH)
tfidf = joblib.load(TFIDF_PATH)
cosine_sim = np.load(COSINE_PATH)

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

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    indices = [i[0] for i in sim_scores]

    recs = books.iloc[indices].copy()
    recs = recs.sort_values("popularity_score", ascending=False)

    return recs[["title", "author", "avg_rating", "rating_count"]]
