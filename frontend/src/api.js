export async function askQuestion(question) {
  const res = await fetch('http://127.0.0.1:8000/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();

  // ✅ ALWAYS return structured fields
  return {
    answer: String(data.answer || ''),
    context_used: String(data.context_used || ''),
  };
}
