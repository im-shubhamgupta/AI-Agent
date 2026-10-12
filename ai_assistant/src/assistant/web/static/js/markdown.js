// Minimal, XSS-safe markdown renderer. All input is HTML-escaped first;
// only a fixed set of tags is generated, and links are limited to http(s).

const escapeHtml = (s) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
   .replace(/"/g, "&quot;").replace(/'/g, "&#39;");

function inline(text) {
  return text
    .replace(/`([^`\n]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>")
    .replace(/\[([^\]\n]+)\]\((https?:\/\/[^\s)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
}

/** Hide model "thinking" blocks (<think>…</think>), including an unfinished one. */
export function stripThinking(text) {
  return text.replace(/<think>[\s\S]*?(<\/think>|$)/g, "").trimStart();
}

/** Convert markdown text to safe HTML. */
export function renderMarkdown(raw) {
  const text = escapeHtml(stripThinking(raw));
  const out = [];
  const parts = text.split(/```/);

  parts.forEach((part, i) => {
    if (i % 2 === 1) {
      // Fenced code block: drop the optional language line.
      out.push(`<pre><code>${part.replace(/^[\w+-]*\n/, "").replace(/\n$/, "")}</code></pre>`);
      return;
    }
    let list = null;
    const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };

    for (const block of part.split(/\n{2,}/)) {
      for (const line of block.split("\n")) {
        const ul = line.match(/^\s*[-*]\s+(.*)/);
        const ol = line.match(/^\s*\d+\.\s+(.*)/);
        const h = line.match(/^(#{1,6})\s+(.*)/);
        if (ul || ol) {
          const tag = ul ? "ul" : "ol";
          if (list !== tag) { closeList(); out.push(`<${tag}>`); list = tag; }
          out.push(`<li>${inline((ul || ol)[1])}</li>`);
        } else if (h) {
          closeList();
          const level = Math.min(h[1].length + 2, 6);
          out.push(`<h${level}>${inline(h[2])}</h${level}>`);
        } else if (line.trim()) {
          closeList();
          out.push(`<p>${inline(line)}</p>`);
        }
      }
      closeList();
    }
  });
  return out.join("");
}
