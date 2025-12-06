# src/app.py
"""
CineMind — Streamlit UI (content-based recommender)
Drop this file into src/app.py (replace existing). It:
 - loads .env from project root
 - safely checks/loads processed data
 - caches TF-IDF matrix
 - optionally shows TMDB posters when TMDB_API_KEY is present
 - provides friendly error messages
"""
import os
from pathlib import Path

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from dotenv import load_dotenv

# local imports (must run from project root)
from src.content_based import build_tfidf_matrix, get_similar_movies
from src.utils import search_movie_tmdb, poster_url_from_tmdb_result

# -----------------------
# setup
# -----------------------
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")                 # load .env from project root
DATA_PATH = ROOT / "data" / "processed" / "cleaned_data.csv"

st.set_page_config(page_title="CineMind — Movie Recommender", layout="wide")
st.title("🎬 CineMind — Content-based Movie Recommender")

# -----------------------
# basic file checks
# -----------------------
if not DATA_PATH.exists():
    st.error(f"Processed data not found. Run preprocessing first and place the csv at:\n\n`{DATA_PATH}`")
    st.stop()

# read CSV (small memory hit once)
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.exception(f"Failed to read processed data: {e}")
    st.stop()

# -----------------------
# cache: TF-IDF matrix (heavy op)
# -----------------------
@st.cache_data(ttl=24 * 3600)
def prepare_matrix(dataframe: pd.DataFrame):
    """
    Build TF-IDF matrix and return it.
    This is cached by Streamlit so repeated reloads are quick.
    """
    tfidf_matrix, vectorizer = build_tfidf_matrix(dataframe)
    return tfidf_matrix

with st.spinner("Building / loading feature matrix..."):
    try:
        tfidf_matrix = prepare_matrix(df)
    except Exception as e:
        st.exception(f"Error building TF-IDF matrix: {e}")
        st.stop()

# -----------------------
# sidebar controls
# -----------------------
tmdb_key = os.getenv("TMDB_API_KEY")
default_show_posters = True if tmdb_key else False

with st.sidebar:
    st.header("Search / Settings")
    movie_query = st.text_input("Movie title", value="Inception")
    top_n = st.slider("Number of recommendations", 5, 20, 10)
    show_posters = st.checkbox("Show posters (requires TMDB API key)", value=default_show_posters)
    st.markdown("---")
    if tmdb_key:
        st.markdown("TMDB key detected — posters enabled if checkbox is ON.")
    else:
        st.markdown("No TMDB key found. To enable posters, put `TMDB_API_KEY=your_key` in a `.env` at project root.")
    st.markdown("Tip: Use exact movie titles for best results (case-insensitive).")

# -----------------------
# main: recommendations
# -----------------------
if not movie_query:
    st.info("Type a movie title in the sidebar to get recommendations.")
    st.stop()

try:
    recs = get_similar_movies(movie_query, df, tfidf_matrix, top_n=top_n)
except ValueError as ve:
    # content-based helper may raise on missing title
    st.error(str(ve))
    st.stop()
except Exception as e:
    st.exception(f"Unexpected error while searching recommendations: {e}")
    st.stop()

st.subheader(f"Top {top_n} recommendations for **{movie_query}**")

# render recommendations
for rank, (title, idx, score) in enumerate(recs, start=1):
    poster_url = None
    if show_posters and tmdb_key:
        # try to fetch poster, but never crash the UI if TMDB fails
        try:
            result = search_movie_tmdb(title)
            poster_url = poster_url_from_tmdb_result(result) if result else None
        except Exception:
            poster_url = None

    cols = st.columns([1, 4])
    with cols[0]:
        if poster_url:
            st.image(poster_url, width=150)
        else:
            st.markdown("🖼️ No poster")
    with cols[1]:
        st.markdown(f"**{rank}. {title}** — score: `{score:.4f}`")
        # show metadata if present
        meta_parts = []
        if "release_year" in df.columns:
            meta_parts.append(f"Release: {df.at[idx,'release_year'] if pd.notna(df.at[idx,'release_year']) else '-'}")
        if "listed_in" in df.columns:
            meta_parts.append(f"Genres: {df.at[idx,'listed_in'] if pd.notna(df.at[idx,'listed_in']) else '-'}")
        if meta_parts:
            st.markdown("  \n".join(meta_parts))
    st.divider()

# -----------------------
# footer / debug (collapsed)
# -----------------------
with st.expander("About / Debug"):
    st.markdown(
        """
        **CineMind** runs a TF-IDF + cosine-similarity content-based recommender.
        - Data location: `{}`  
        - TMDB key loaded: {}  
        - Number of titles in dataset: {}
        """.format(DATA_PATH, bool(tmdb_key), len(df))
    )
    if st.checkbox("Show raw recommendations (debug)"):
        st.write(recs)
