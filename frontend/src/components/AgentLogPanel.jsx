export default function AgentLogPanel({ logs }) {
  return (
    <aside className="log-panel">
      <div className="panel-heading">
        <span>Agent Decision Log</span>
        <strong>{logs.length}</strong>
      </div>

      <div className="log-list">
        {logs.length === 0 && (
          <p className="empty-log">Agent traces will appear after the first player message.</p>
        )}
        {logs.map((entry, index) => (
          <article className="log-entry" key={`${entry.agent}-${index}`}>
            <h3>{entry.agent}</h3>
            <p>{entry.reasoning_summary}</p>
            <pre>{JSON.stringify(entry.output, null, 2)}</pre>
          </article>
        ))}
      </div>
    </aside>
  );
}
