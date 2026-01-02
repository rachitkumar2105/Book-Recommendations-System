import pandas as pd
df = pd.read_csv("artifacts/books_metadata.csv")
cols = [c for c in df.columns if 'image' in c.lower()]
print("IMAGE COLUMNS:", cols)
print("ALL COLUMNS:", df.columns.tolist())
