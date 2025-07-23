import axios from 'axios';
import { useState } from 'react';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const ask = async () => {
    const formData = new FormData();
    formData.append('query', question);
    const res = await axios.post('http://localhost:8000/chat', formData);
    setAnswer(res.data.answer);
  };

  return (
    <div className="p-4">
      <input
        className="border px-2 py-1 w-full"
        placeholder="Ask a question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={ask} className="bg-green-600 text-white px-4 py-2 mt-2">Ask</button>
      <p className="mt-4 bg-gray-100 p-3">{answer}</p>
    </div>
  );
}