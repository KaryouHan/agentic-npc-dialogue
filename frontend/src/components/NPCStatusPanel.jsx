import aliceAvatar from '../assets/alice-avatar.png';

function StatBar({ label, value, tone }) {
  return (
    <div className="stat-row">
      <div className="stat-label">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
      <div className="stat-track">
        <div className={`stat-fill ${tone}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

export default function NPCStatusPanel({ npcState, expression, currentAction }) {
  const state = npcState ?? {
    name: 'アリス',
    fear: 80,
    trust: 20,
    anger: 10,
    quest_state: 'not_started',
    has_key: true,
    relationship: 'stranger',
  };

  return (
    <aside className="npc-panel">
      <div className={`portrait ${expression}`}>
        <img src={aliceAvatar} alt="アリス" />
      </div>

      <div className="npc-title">
        <span>NPC</span>
        <h2>{state.name}</h2>
      </div>

      <dl className="meta-list">
        <div>
          <dt>Expression</dt>
          <dd>{expression}</dd>
        </div>
        <div>
          <dt>Quest</dt>
          <dd>{state.quest_state}</dd>
        </div>
        <div>
          <dt>Action</dt>
          <dd>{currentAction}</dd>
        </div>
        <div>
          <dt>Key</dt>
          <dd>{state.has_key ? 'holding' : 'given'}</dd>
        </div>
        <div>
          <dt>Relation</dt>
          <dd>{state.relationship}</dd>
        </div>
      </dl>

      <div className="stats">
        <StatBar label="fear" value={state.fear} tone="fear" />
        <StatBar label="trust" value={state.trust} tone="trust" />
        <StatBar label="anger" value={state.anger} tone="anger" />
      </div>
    </aside>
  );
}
