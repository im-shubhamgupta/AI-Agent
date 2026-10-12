// Tiny state holder: current session id (persisted so a refresh keeps the chat).

const KEY = "assistant.sessionId";

export const newSessionId = () => crypto.randomUUID().replace(/-/g, "");

export function currentSessionId() {
  try {
    let id = localStorage.getItem(KEY);
    if (!id) { id = newSessionId(); localStorage.setItem(KEY, id); }
    return id;
  } catch {
    return newSessionId();
  }
}

export function setSessionId(id) {
  try { localStorage.setItem(KEY, id); } catch { /* storage unavailable */ }
}
