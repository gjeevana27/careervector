from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")

index = pc.Index("jd-matcher")
print("Connected to Pinecone index: jd-matcher")

# Load jobs
df = pd.read_csv("data/jobs.csv")
print(f"Ingesting {len(df)} job descriptions...")

# Clean nan values before ingestion
df = df.fillna("")

# Remove rows with empty descriptions
df = df[df["full_description"].str.strip() != ""]
df = df[df["full_description"].str.len() > 100]
df = df.reset_index(drop=True)

print(f"After cleaning: {len(df)} valid job descriptions")

batch_size = 50
total_batches = (len(df) + batch_size - 1) // batch_size

for i in range(0, len(df), batch_size):

    batch = df.iloc[i:i+batch_size]
    batch_num = i // batch_size + 1

    # Combine title + description for richer embedding
    texts = (
        batch["title"].fillna("") + ". " +
        batch["full_description"].fillna("")
    ).tolist()

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    ).tolist()

    vectors = []
    for j, (_, row) in enumerate(batch.iterrows()):

        # Clean each field — convert nan to empty string
        def safe(val, limit=None):
            result = str(val) if val and str(val).lower() != "nan" else ""
            return result[:limit] if limit else result

        vectors.append({
            "id": safe(row.get("id")),
            "values": embeddings[j],
            "metadata": {
                "title":            safe(row.get("title")),
                "company":          safe(row.get("company")),
                "location":         safe(row.get("location")),
                "required_skills":  safe(row.get("required_skills"), 500),
                "full_description": safe(row.get("full_description"), 1000),
                "employment_type":  safe(row.get("employment_type")),
                "is_remote":        bool(row.get("is_remote", False)),
                "apply_link":       safe(row.get("apply_link")),
                "posted_at":        safe(row.get("posted_at"))
            }
        })

    # Skip vectors with empty IDs
    vectors = [v for v in vectors if v["id"]]

    if vectors:
        index.upsert(vectors=vectors)

    print(
        f"Batch {batch_num}/{total_batches} done — "
        f"{min(i+batch_size, len(df))}/{len(df)} jobs"
    )

stats = index.describe_index_stats()
print(f"\nDone! Total vectors in Pinecone: {stats['total_vector_count']}")