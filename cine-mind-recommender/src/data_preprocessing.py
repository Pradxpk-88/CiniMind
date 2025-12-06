import argparse
import pandas as pd
from pathlib import Path

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"🔍 Data loaded: {df.shape}  ({path})")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df = df.dropna(subset=['title'])

    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    if 'cast' in df.columns:
        df['cast'] = df['cast'].fillna('')

    text_cols = [c for c in ['title', 'director', 'cast', 'listed_in', 'description'] if c in df.columns]
    df['combined_text'] = df[text_cols].astype(str).agg(' '.join, axis=1)

    print(f"🧼 Data cleaned: {df.shape}")
    return df

def save_processed(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"💾 Processed data saved: {path}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/netflix_titles.csv")
    parser.add_argument("--output", default="data/processed/cleaned_data.csv")
    return parser.parse_args()

def main():
    args = parse_args()
    df = load_data(Path(args.input))
    df = clean_data(df)
    save_processed(df, Path(args.output))

if __name__ == "__main__":
    main()
