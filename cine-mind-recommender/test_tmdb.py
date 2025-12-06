# test_tmdb.py — safe tester, prints minimal info
print("RUNNING test_tmdb.py")

from pathlib import Path
from dotenv import load_dotenv
import os, requests, json

ROOT = Path(__file__).resolve().parents[0]
load_dotenv(ROOT / ".env")

key = os.getenv("TMDB_API_KEY")
print("HAS_KEY:", bool(key))

if not key:
    print("NO_KEY")
    raise SystemExit(0)

resp = requests.get("https://api.themoviedb.org/3/search/movie", params={"api_key": key, "query": "Inception"})
print("STATUS_CODE:", resp.status_code)

try:
    data = resp.json().get("results", [])
    if not data:
        print("NO_RESULTS")
    else:
        first = data[0]
        print("FIRST_TITLE:", first.get("title"))
        print("FIRST_POSTER_PATH:", first.get("poster_path"))
except Exception as e:
    print("JSON_ERR:", str(e))
