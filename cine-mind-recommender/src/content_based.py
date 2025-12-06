# src/content_based.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def ensure_text_column(df: pd.DataFrame, col_name="combined_text"):
    """Make sure the dataframe has a text column we can vectorize."""
    if col_name not in df.columns:
        text_cols = [c for c in ["title", "director", "cast", "listed_in", "description"] if c in df.columns]
        df["description"] = df.get("description", "").fillna("")
        df[col_name] = df[text_cols].astype(str).agg(" ".join, axis=1)
    return df

def build_tfidf_matrix(df: pd.DataFrame, text_col="combined_text", max_features: int = 20000):
    """
    Build TF-IDF vectorizer + matrix from dataframe.
    Returns: (tfidf_matrix, vectorizer)
    """
    df = ensure_text_column(df, text_col)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(df[text_col].astype(str))
    return tfidf_matrix, vectorizer

def _find_best_index_for_query(df: pd.DataFrame, query: str):
    # Try case-insensitive substring match first
    q = query.strip().lower()
    if q == "":
        raise ValueError("Empty query provided.")
    matches = df[df["title"].str.lower().str.contains(q, na=False)]
    if not matches.empty:
        return int(matches.index[0])
    # fallback to exact case-insensitive match
    exact = df[df["title"].str.lower() == q]
    if not exact.empty:
        return int(exact.index[0])
    # fallback to partial token match
    toks = [t for t in q.split() if len(t) > 2]
    for t in toks:
        m = df[df["title"].str.lower().str.contains(t, na=False)]
        if not m.empty:
            return int(m.index[0])
    raise ValueError(f"Title not found: '{query}'. Try a different query or use an exact title from the dataset.")

def get_similar_movies(query: str, df: pd.DataFrame, tfidf_matrix, top_n: int = 10):
    """
    Given a text query (movie title), dataframe, and precomputed TF-IDF matrix,
    return a list of (title, index, score) for top_n similar items.
    """
    if isinstance(tfidf_matrix, tuple):  # guard if user passed (matrix, vec)
        tfidf_matrix = tfidf_matrix[0]

    idx = _find_best_index_for_query(df, query)
    query_vec = tfidf_matrix[idx]
    cosine_sim = linear_kernel(query_vec, tfidf_matrix).flatten()
    scores = list(enumerate(cosine_sim))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # exclude self
    recs = [(df.iloc[i]["title"], int(i), float(score)) for i, score in scores if i != idx][:top_n]
    return recs
