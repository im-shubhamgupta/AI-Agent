// Entry point: wires the DOM events to the API and UI modules.
import * as api from "./api.js";
import { currentSessionId, newSessionId, setSessionId } from "./state.js";
import * as ui from "./ui.js";

const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const app = document.querySelector(".app");

let sessionId = currentSessionId();
let busy = false;

function setBusy(value) {
  busy = value;
  sendBtn.disabled = value;
  input.disabled = value;
  if (!value) input.focus();
}

function autoGrow() {
  input.style.height = "auto";
  input.style.height = `${input.scrollHeight}px`;
}

async function refreshSessions() {
  try {
    const sessions = await api.listSessions();
    ui.renderSessions(sessions, sessionId, { onOpen: openSession, onDelete: removeSession });
  } catch { /* sidebar is non-critical */ }
}

async function openSession(id) {
  if (busy) return;
  sessionId = id;
  setSessionId(id);
  ui.clearMessages();
  try {
    for (const m of await api.getMessages(id)) {
      if (m.role === "user") ui.addUserMessage(m.content);
      else ui.addAssistantMessage(m.content);
    }
  } catch { /* show empty chat */ }
  app.classList.remove("sidebar-open");
  refreshSessions();
}

async function removeSession(id) {
  if (busy) return;
  try { await api.deleteSession(id); } catch { return; }
  if (id === sessionId) startNewChat();
  else refreshSessions();
}

function startNewChat() {
  if (busy) return;
  sessionId = newSessionId();
  setSessionId(sessionId);
  ui.clearMessages();
  app.classList.remove("sidebar-open");
  refreshSessions();
  input.focus();
}

async function send(text) {
  ui.addUserMessage(text);
  const reply = ui.startAssistantReply(); // shows the preloader
  setBusy(true);
  try {
    await api.streamChat(sessionId, text, { onToken: reply.update });
    reply.finish();
  } catch (err) {
    reply.fail(err.message || "Something went wrong. Please try again.");
  } finally {
    setBusy(false);
    refreshSessions();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text || busy) return;
  input.value = "";
  autoGrow();
  send(text);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    form.requestSubmit();
  }
});
input.addEventListener("input", autoGrow);

document.getElementById("new-chat").addEventListener("click", startNewChat);
document.getElementById("toggle-sidebar").addEventListener("click", () => {
  if (window.matchMedia("(max-width: 720px)").matches) app.classList.toggle("sidebar-open");
  else app.classList.toggle("sidebar-hidden");
});

openSession(sessionId);
