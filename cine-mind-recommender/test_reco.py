import pandas as pd
from src.content_based import build_tfidf_matrix, get_similar_movies
df = pd.read_csv('data/processed/cleaned_data.csv')
mat, vec = build_tfidf_matrix(df)
print(get_similar_movies('21', df, mat, top_n=5))
