const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}

export function fetchState() {
  return request('/api/state');
}

export function sendDialogue(message) {
  return request('/api/dialogue', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

export function resetDemo() {
  return request('/api/reset', {
    method: 'POST',
  });
}
