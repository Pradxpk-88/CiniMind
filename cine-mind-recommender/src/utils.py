# src/utils.py
import os
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path

# load .env from project root (safe even if already loaded)
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"

def get_tmdb_key():
    return os.getenv("TMDB_API_KEY")

def search_movie_tmdb(title):
    key = get_tmdb_key()
    if not key:
        return None
    q = quote_plus(title)
    url = "https://api.themoviedb.org/3/search/movie"
    try:
        resp = requests.get(url, params={"api_key": key, "query": title}, timeout=10)
        resp.raise_for_status()
    except Exception:
        return None
    data = resp.json().get("results", [])
    return data[0] if data else None

def poster_url_from_tmdb_result(result, size="w300"):
    if not result:
        return None
    poster_path = result.get("poster_path")
    if not poster_path:
        return None
    return f"{TMDB_IMAGE_BASE}/{size}{poster_path}"
