# backend/rag/ingest.py

import pandas as pd
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# --------------------------
# 1️⃣ Paths setup
# --------------------------
# Project structure:
# backend/data/jobs.csv
# backend/storage/ -> where we save FAISS index and job_ids

base_path = Path(__file__).parent.parent  # backend/
data_path = base_path / "data" / "jobs.csv"
storage_path = base_path / "storage"
storage_path.mkdir(exist_ok=True)  # create storage folder if not exists

faiss_index_file = storage_path / "faiss_index.jobs"
job_ids_file = storage_path / "job_ids.pkl"

# --------------------------
# 2️⃣ Load jobs dataset
# --------------------------
if not data_path.exists():
    raise FileNotFoundError(f"CSV not found at {data_path}")

df = pd.read_csv(data_path)
print("✅ CSV loaded successfully!")

# --------------------------
# 3️⃣ Convert each row into text
# --------------------------
job_texts = []
job_ids = []

for _, row in df.iterrows():
    text = (
        f"Job ID: {row['job_id']}\n"
        f"Type: {row['job_type']}\n"
        f"Location: {row['location']}\n"
        f"Language: {row['language']}\n"
        f"Salary: {row['salary']}\n"
        f"Safety: {row['safety_level']}\n"
        f"Distance: {row['distance_km']} km\n"
        f"Stay Available: {row['stay_available']}\n"
    )
    job_texts.append(text)
    job_ids.append(row['job_id'])

print(f"✅ Converted {len(job_texts)} jobs into text.")

# --------------------------
# 4️⃣ Generate embeddings (no API key needed)
# --------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(job_texts)
emb_array = np.array(embeddings).astype('float32')
print("✅ Embeddings generated.")

# --------------------------
# 5️⃣ Create FAISS index
# --------------------------
dimension = emb_array.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(emb_array)
print(f"✅ FAISS index created with {index.ntotal} vectors.")

# --------------------------
# 6️⃣ Save index and job IDs to storage/
# --------------------------
faiss.write_index(index, str(faiss_index_file))

with open(job_ids_file, "wb") as f:
    pickle.dump(job_ids, f)

print(f"✅ FAISS index saved at: {faiss_index_file}")
print(f"✅ Job IDs saved at: {job_ids_file}")
print("✅ RAG ingestion complete!")
