import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface: React.FC = () => {
    const [question, setQuestion] = useState("");
    const [history, setHistory] = useState<{ sender: 'user' | 'bot', text: string }[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!question.trim()) return;

        const currentQuestion = question;
        setQuestion("");
        setHistory(prev => [...prev, { sender: 'user', text: currentQuestion }]);
        setLoading(true);

        try {
            const res = await axios.post('http://localhost:8000/api/chat', { question: currentQuestion });
            setHistory(prev => [...prev, { sender: 'bot', text: res.data.answer }]);
        } catch (err) {
            console.error(err);
            setHistory(prev => [...prev, { sender: 'bot', text: "Error getting response." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card chat-card">
            <h2>Chat with Candidate Resume</h2>
            <div className="chat-window">
                {history.length === 0 && <p className="placeholder">Ask questions like "Does he know Python?" or "What is his degree?"</p>}
                {history.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        <strong>{msg.sender === 'user' ? 'You' : 'AI'}: </strong>
                        {msg.text}
                    </div>
                ))}
                {loading && <div className="message bot"><em>Thinking...</em></div>}
            </div>

            <div className="chat-input">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Ask a question..."
                />
                <button onClick={handleSend} disabled={loading}>Send</button>
            </div>
        </div>
    );
};

export default ChatInterface;
