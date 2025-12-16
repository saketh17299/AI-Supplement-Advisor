import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: query }),
      });

      const data = await res.json();
      console.log('API response:', data);
      setResponse(data);
    } catch (err) {
      console.error('Error fetching answer:', err);
      setResponse({ answer: 'Error fetching answer', context_used: '' });
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: {
      maxWidth: 800,
      margin: '0 auto',
      padding: 20,
      fontFamily: 'Arial, sans-serif',
    },
    input: { width: '80%', padding: 10, fontSize: 16, marginRight: 10 },
    button: {
      padding: '10px 20px',
      fontSize: 16,
      background: 'Green',
      color: 'white',
      borderRadius: 50,
    },
    card: {
      marginTop: 20,
      padding: 20,
      border: '1px solid #ccc',
      borderRadius: 8,
      background: '#f9f9f9',
    },
    context: { whiteSpace: 'pre-wrap', color: '#555' },
  };

  return (
    <div style={styles.container}>
      <h1>AI Supplement Advisor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask about a supplement..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>

      {response && (
        <div style={styles.card}>
          <h3>Answer:</h3>
          <p>{String(response.answer.answer)}</p>

          <h4>Context Used:</h4>
          <p style={styles.context}>
            {response.answer.context_used
              ? String(response.answer.context_used)
              : 'No context available'}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
