import { useEffect, useMemo, useState } from 'react';
import { RotateCcw } from 'lucide-react';
import { fetchState, resetDemo, sendDialogue } from './api.js';
import AgentLogPanel from './components/AgentLogPanel.jsx';
import ChatWindow from './components/ChatWindow.jsx';
import NPCStatusPanel from './components/NPCStatusPanel.jsx';

const openingMessage = {
  role: 'alice',
  content: '......誰？ 近づかないで。あなたも追っ手なの？',
};

export default function App() {
  const [npcState, setNpcState] = useState(null);
  const [messages, setMessages] = useState([openingMessage]);
  const [agentLog, setAgentLog] = useState([]);
  const [currentAction, setCurrentAction] = useState('hesitate');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchState()
      .then((data) => {
        setNpcState(data.current_state);
        setMessages(data.history.length ? data.history : [openingMessage]);
      })
      .catch((err) => setError(err.message));
  }, []);

  const expression = useMemo(() => {
    if (!npcState) return 'unknown';
    if (npcState.anger >= 65) return 'angry';
    if (npcState.trust >= 70) return 'trusting';
    if (npcState.fear >= 65) return 'afraid';
    if (npcState.trust >= 45) return 'guarded';
    return 'anxious';
  }, [npcState]);

  async function handleSend(message) {
    setLoading(true);
    setError('');
    setMessages((current) => [...current, { role: 'player', content: message }]);

    try {
      const response = await sendDialogue(message);
      setNpcState(response.current_state);
      setCurrentAction(response.action);
      setAgentLog(response.agent_log);
      setMessages((current) => [...current, { role: 'alice', content: response.reply }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleReset() {
    setLoading(true);
    setError('');
    try {
      const data = await resetDemo();
      setNpcState(data.current_state);
      setMessages([openingMessage]);
      setAgentLog([]);
      setCurrentAction('hesitate');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="scene-header">
        <div>
          <p className="eyebrow">Abandoned Magic Academy</p>
          <h1>Agentic AI NPC Dialogue System</h1>
        </div>
        <button className="icon-button" type="button" onClick={handleReset} title="Reset demo">
          <RotateCcw size={18} />
        </button>
      </section>

      <section className="game-layout">
        <NPCStatusPanel
          npcState={npcState}
          expression={expression}
          currentAction={currentAction}
        />
        <ChatWindow messages={messages} onSend={handleSend} loading={loading} error={error} />
        <AgentLogPanel logs={agentLog} />
      </section>
    </main>
  );
}
