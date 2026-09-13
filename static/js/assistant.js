(function () {
  const toggle = document.getElementById('skillup-agent-toggle');
  const panel = document.getElementById('skillup-agent-panel');
  const close = document.getElementById('skillup-agent-close');
  const form = document.getElementById('skillup-agent-form');
  const input = document.getElementById('skillup-agent-input');
  const messages = document.getElementById('skillup-agent-messages');
  if (!toggle || !panel || !close || !form || !input || !messages) return;

  function addMessage(text, type) {
    const message = document.createElement('div');
    message.className = 'agent-message ' + type;
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }

  async function ask(question) {
    addMessage(question, 'user');
    try {
      const response = await fetch('/api/assistant', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question})
      });
      const data = await response.json();
      addMessage(data.answer || 'I could not find an answer in the project context.', 'agent');
    } catch (error) {
      addMessage('The assistant service is unavailable. Check that the Flask server is running.', 'agent');
    }
  }

  function setOpen(open) {
    panel.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    if (open) input.focus();
  }

  toggle.addEventListener('click', () => setOpen(panel.hidden));
  close.addEventListener('click', () => setOpen(false));
  document.querySelectorAll('[data-agent-question]').forEach(button => button.addEventListener('click', () => ask(button.dataset.agentQuestion)));
  form.addEventListener('submit', event => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;
    input.value = '';
    ask(question);
  });
})();
