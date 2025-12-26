# backend/evaluation/groundedness.py
def groundedness_score(answer, context):
    supported = [
        s for s in answer.split(".")
        if s.strip() and s.lower() in context.lower()
    ]
    return len(supported) / max(len(answer.split(".")), 1)
