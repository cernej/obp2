const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(role, text) {
  const wrapper = document.createElement('article');
  wrapper.className = `msg msg-${role}`;

  const badge = document.createElement('h3');
  badge.textContent = role === 'user' ? 'Ty' : 'AI asistent';

  const body = document.createElement('p');
  body.textContent = text;

  wrapper.appendChild(badge);
  wrapper.appendChild(body);
  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Neznamy problem pri komunikaci se serverem.');
  }

  return data.answer;
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) {
    return;
  }

  addMessage('user', message);
  chatInput.value = '';
  chatInput.style.height = 'auto';
  sendBtn.disabled = true;
  addMessage('assistant', 'Premyslim...');

  try {
    const answer = await sendMessage(message);
    chatWindow.lastChild.remove();
    addMessage('assistant', answer);
  } catch (error) {
    chatWindow.lastChild.remove();
    addMessage('assistant', `Chyba: ${error.message}`);
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
});

chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = `${Math.min(chatInput.scrollHeight, 220)}px`;
});

addMessage('assistant', 'Ahoj, jsem tvuj AI asistent. Na co se chces zeptat?');