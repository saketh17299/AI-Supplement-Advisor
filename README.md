## System Architecture
graph TD
    UserQ[User Query] --> API[FastAPI]
    API --> RAG[RAG Engine]

    RAG --> VDB[(Qdrant)]
    RAG --> LLM[Groq]

    RAG --> RESP[Response]
    RESP --> FE[Frontend]

    RAG --> METRICS[Evaluation Layer]
    METRICS --> Recall[Recall@K]
    METRICS --> Ground[Groundedness]
    METRICS --> Latency[Latency]

    METRICS --> Logs[(Metrics Store)]
    Designed and implemented an end to end RAG based AI system with vector search, prompt engineering, evaluation metrics, and scalable API architecture.
