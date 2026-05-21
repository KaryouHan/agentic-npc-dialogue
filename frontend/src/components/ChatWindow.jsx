import { Send } from 'lucide-react';
import { useState } from 'react';

export default function ChatWindow({ messages, onSend, loading, error }) {
  const [draft, setDraft] = useState('');

  function submit(event) {
    event.preventDefault();
    const message = draft.trim();
    if (!message || loading) return;
    setDraft('');
    onSend(message);
  }

  return (
    <section className="chat-panel">
      <div className="chat-scroll">
        {messages.map((message, index) => (
          <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
            <span className="speaker">{message.role === 'player' ? 'Player' : 'アリス'}</span>
            <p>{message.content}</p>
          </div>
        ))}
        {loading && (
          <div className="message alice">
            <span className="speaker">アリス</span>
            <p>......</p>
          </div>
        )}
      </div>

      {error && <p className="error-line">{error}</p>}

      <form className="input-row" onSubmit={submit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="自由に入力: 私はあなたを助けに来た。"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !draft.trim()} title="Send message">
          <Send size={18} />
        </button>
      </form>
    </section>
  );
}
