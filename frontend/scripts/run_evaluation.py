from backend.rag import generate_answer
from backend.evaluation.recall import recall_at_k
from backend.evaluation.groundedness import groundedness_score

EVAL_SET = [
    {
        "query": "Can I use creatine for muscle gain?",
        "relevant_docs": ["Creatine helps improve strength and muscle mass."]
    }
]

for item in EVAL_SET:
    response = generate_answer(item["query"])

    recall = recall_at_k(item["query"], item["relevant_docs"])
    grounded = groundedness_score(
        response["answer"], response["context_used"]
    )

    print("Query:", item["query"])
    print("Recall@3:", recall)
    print("Groundedness:", grounded)
    print("-" * 40)
