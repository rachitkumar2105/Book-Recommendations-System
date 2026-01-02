import joblib
import pandas as pd
import scipy.sparse

try:
    obj = joblib.load("artifacts/tfidf.pkl")
    print(f"Type: {type(obj)}")
    if hasattr(obj, 'shape'):
        print(f"Shape: {obj.shape}")
    if scipy.sparse.issparse(obj):
        print("It is a sparse matrix.")
except Exception as e:
    print(f"Error: {e}")
