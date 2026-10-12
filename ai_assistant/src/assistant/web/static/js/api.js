// All network calls live here.

async function json(res) {
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.status === 204 ? null : res.json();
}

export const listSessions = () => fetch("/api/sessions").then(json);
export const getMessages = (id) => fetch(`/api/sessions/${encodeURIComponent(id)}/messages`).then(json);
export const deleteSession = (id) =>
  fetch(`/api/sessions/${encodeURIComponent(id)}`, { method: "DELETE" }).then(json);

/**
 * Send a message and stream the reply.
 * @param {string} sessionId
 * @param {string} message
 * @param {{onToken: (t: string) => void, signal?: AbortSignal}} opts
 * @throws {Error} on network failure or an error event from the server.
 */
export async function streamChat(sessionId, message, { onToken, signal }) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
    signal,
  });
  if (!res.ok || !res.body) throw new Error(`Request failed (${res.status})`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop();
    for (const evt of events) {
      if (!evt.startsWith("data: ")) continue;
      const data = JSON.parse(evt.slice(6));
      if (data.error) throw new Error(data.error);
      if (data.token) onToken(data.token);
    }
  }
}
