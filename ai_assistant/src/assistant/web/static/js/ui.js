// DOM helpers: rendering messages, the preloader, and the session list.
import { renderMarkdown } from "./markdown.js";

const $ = (id) => document.getElementById(id);
const messagesEl = $("messages");
const emptyEl = $("empty");

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function messageNode(role) {
  const wrap = el("div", `message ${role}`);
  wrap.append(el("div", "avatar", role === "user" ? "You" : "AI"));
  const body = el("div", "body");
  wrap.append(body);
  emptyEl.classList.add("hidden");
  messagesEl.append(wrap);
  return { wrap, body };
}

export function clearMessages() {
  messagesEl.querySelectorAll(".message").forEach((n) => n.remove());
  emptyEl.classList.remove("hidden");
}

export function addUserMessage(text) {
  messageNode("user").body.textContent = text;
  scrollToBottom();
}

export function addAssistantMessage(text) {
  messageNode("assistant").body.innerHTML = renderMarkdown(text);
  scrollToBottom();
}

/** Create an assistant bubble showing the preloader (typing dots). */
export function startAssistantReply() {
  const { wrap, body } = messageNode("assistant");
  const loader = el("div", "typing");
  loader.setAttribute("role", "status");
  loader.setAttribute("aria-label", "Assistant is typing");
  loader.append(el("span"), el("span"), el("span"));
  body.append(loader);
  scrollToBottom();

  let text = "";
  return {
    /** Append streamed text; the first call replaces the preloader. */
    update(chunk) {
      text += chunk;
      body.innerHTML = renderMarkdown(text);
      scrollToBottom();
    },
    fail(message) {
      wrap.classList.add("error");
      body.textContent = message;
    },
    /** Remove the preloader if no text ever arrived. */
    finish() {
      if (!text && !wrap.classList.contains("error")) body.textContent = "(no response)";
    },
  };
}

export function renderSessions(sessions, activeId, { onOpen, onDelete }) {
  const list = $("session-list");
  list.replaceChildren();
  for (const s of sessions) {
    const item = el("div", `session-item${s.id === activeId ? " active" : ""}`);
    const open = el("button", "session-open", s.title);
    open.type = "button";
    open.addEventListener("click", () => onOpen(s.id));
    const del = el("button", "session-delete", "✕");
    del.type = "button";
    del.setAttribute("aria-label", "Delete chat");
    del.addEventListener("click", () => onDelete(s.id));
    item.append(open, del);
    list.append(item);
  }
}
