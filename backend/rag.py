# backend/rag.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from groq import Groq

load_dotenv()

# -----------------------------
# CONFIG
# -----------------------------
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "supplements")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------------
# INIT QDRANT CLIENT
# -----------------------------
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# -----------------------------
# INIT FastEmbed EMBEDDER
# -----------------------------
embedder = TextEmbedding()

# -----------------------------
# INIT GROQ CLIENT
# -----------------------------
if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: GROQ_API_KEY is missing. Set it in your environment.")

groq_client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# FUNCTION: Generate answer
# -----------------------------
def generate_answer(query: str) -> dict:
    """
    Generate answer for a user query using Qdrant + Groq (RAG pipeline)
    Returns: dict with 'answer' and 'context_used'
    """
    
    try:
        # 1️⃣ Embed user query
        query_vector = list(embedder.embed([query]))[0]  # list of floats

        # 2️⃣ Search Qdrant collection
        results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=3
        )

        # 3️⃣ Prepare context from top documents
        if not results:
            context_text = "No relevant documents found."
        else:
            context_text = "\n".join([r.payload.get("page_content", "") for r in results])

        # 4️⃣ Prepare prompt for LLM
        
        prompt = f"""
You are an expert AI Supplement Advisor. Your task is to answer the user's question using ONLY the information provided in the context. 
Provide safe, clear, and practical advice. Use simple language and format the answer in readable paragraphs or bullet points. 

Important rules:
- Do not hallucinate or provide information not in the context.
- If the context does not contain relevant information, politely say that the answer is not available.
- Focus on actionable insights, benefits, precautions, and usage if applicable.
- Avoid overly technical language; make it understandable for a general audience.

Context:
{context_text}

User's Question:
{query}

Provide the answer below:
"""

        # 5️⃣ Call Groq LLM
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI Supplement Advisor."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        import re

# Inside generate_answer after getting answer from Groq
        raw_answer = response.choices[0].message.content

# Remove Markdown bold ** and extra whitespace
        clean_answer = re.sub(r"\*\*", "", raw_answer).strip()
        clean_answer = re.sub(r"\*", "\n", clean_answer).strip()

# Optional: Replace multiple newlines with just 2 newlines for better spacing
        clean_answer = re.sub(r"\n\s*\n+", "\n\n", clean_answer)

        return {
                "answer": clean_answer,
                "context_used": context_text
        }


    except Exception as e:
        return {"answer": f"ERROR: {e}", "context_used": ""}
