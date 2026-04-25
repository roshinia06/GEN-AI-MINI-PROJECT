import pandas as pd
import os
from rag.vector_store import add_to_vector_store


def ingest_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "travel_packages.csv")
    df = pd.read_csv(data_path)

    texts = []

    for _, row in df.head(1000).iterrows():
        text = f"{row.get('place', '')} - {row.get('about_trip', '')} - Price: {row.get('price', '')} - Duration: {row.get('time', '')}"
        texts.append(text)

    add_to_vector_store(texts)
