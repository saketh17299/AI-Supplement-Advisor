#!/usr/bin/env python3

# qdrant_client_setup.py
'''import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from fastembed import TextEmbedding

load_dotenv()

# -----------------------------
# CONFIG
# -----------------------------
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "supplements")

# -----------------------------
# DEFAULT SAMPLE DOCUMENTS
# -----------------------------
DOCUMENTS = [
    "Creatine helps improve strength and muscle mass.",
    "Vitamin D3 supports immune function.",
    "Omega-3 reduces inflammation.",
    "Protein powder helps meet daily protein intake.",
    "Magnesium improves sleep and recovery."
]

# -----------------------------
# CONNECT TO QDRANT
# -----------------------------
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)
print("⚡ Connected to Qdrant.")

# -----------------------------
# CREATE COLLECTION IF MISSING
# -----------------------------
def ensure_collection():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        print(f"📦 Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # FastEmbed vector dimension
                distance=Distance.COSINE
            )
        )
        print("✅ Collection created.")
    else:
        print(f"📦 Collection '{COLLECTION_NAME}' already exists.")

# -----------------------------
# EMBED & UPLOAD DOCUMENTS
# -----------------------------
def upload_documents(docs):
    embedder = TextEmbedding()
    vectors = list(embedder.embed(docs))  # convert generator to list

    points = [
        PointStruct(
            id=i,
            vector=vectors[i],
            payload={"page_content": docs[i]}
        )
        for i in range(len(docs))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"✅ {len(docs)} documents uploaded successfully.")

# -----------------------------
# RUN
# -----------------------------
ensure_collection()
upload_documents(DOCUMENTS)
'''
import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from fastembed import TextEmbedding
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Qdrant Setup
# -----------------------------
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "supplements")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# -----------------------------
# Create Collection If Missing
# -----------------------------
def init_collection():
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"📦 Created Qdrant Collection: {COLLECTION_NAME}")
    else:
        print(f"📦 Collection '{COLLECTION_NAME}' already exists!")


# -----------------------------
# Upload Documents From Folder
# -----------------------------
def upload_text_folder(folder_path: str):
    embedder = TextEmbedding()

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not files:
        print("❌ No .txt files found!")
        return

    print(f"📁 Found {len(files)} files. Uploading...")

    batch_points = []

    for idx, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)

        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Create embedding
        vector = list(embedder.embed([content]))[0]

        # Create Qdrant point
        batch_points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={"filename": filename, "page_content": content}
            )
        )

    # Upload to Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=batch_points)

    print(f"✅ Uploaded {len(batch_points)} documents successfully!")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    init_collection()

    folder = "backend/documents"   # Change to folder containing your 50 text files
    upload_text_folder(folder)
