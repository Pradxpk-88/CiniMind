🎬 CineMind – AI Movie Recommender System

CineMind is a content-based movie recommender built using TF-IDF, Cosine Similarity, Streamlit UI, and optional TMDB posters.
Enter a movie → get smart recommendations immediately.

⭐ Features

🔍 Search any movie title
🎞️ (Optional) Movie posters via TMDB API
🧠 TF-IDF similarity engine
🚀 Clean modular code
🎚 Adjustable recommendation count
🖥️ Streamlit web interface

🏗️ Architecture
User → Streamlit UI → (title)
                     ↓
       Content-Based Engine (TF-IDF + Cosine)
                     ↓
     Top-N Movies + Optional Posters via TMDB

📁 Project Structure
cine-mind-recommender/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── app.py
│   ├── content_based.py
│   ├── data_preprocessing.py
│   ├── utils.py
│   └── __init__.py
│
├── requirements.txt
├── .env
└── README.md

🛠️ Installation
1️⃣ Clone repo
git clone https://github.com/your-username/cine-mind-recommender.git
cd cine-mind-recommender

2️⃣ Create environment
conda create -n cinemind python=3.10 -y
conda activate cinemind

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Optional: TMDB API (for posters)

Create .env in project folder:

TMDB_API_KEY=your_key_here


You can get the key from:
https://www.themoviedb.org/

If no key is set → app still works, just no posters.

▶️ Run the App
python -m streamlit run src/app.py


App opens at:
http://localhost:8501

🧠 How Recommendations Work

Combine movie metadata → title + description + cast + genres

Convert text to vectors using TF-IDF

Compute similarity with cosine similarity

Pick the top-N closest matches

(Optional) Fetch poster from TMDB

🚀 Future Upgrades

Hybrid recommender (collaborative + content-based)

Auto-complete movie search

Filter by genre, year

Deployment to Render / Streamlit Cloud

👨‍💻 Author

Pradeep Kumar (Leon)
AI & Data Science | Always building 🔥 projects

⭐ Support

If this project helped you, drop a ⭐ on GitHub — it helps your portfolio shine.