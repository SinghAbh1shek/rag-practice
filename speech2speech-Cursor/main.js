// Simple chat simulation (client-side only - no server interaction)

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Function to add a message to the chat display
function addMessage(message, isUser) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  if (isUser) {
    messageElement.classList.add('user-message');
  } else {
    messageElement.classList.add('other-user-message');
  }
  messageElement.textContent = message;
  chatMessages.appendChild(messageElement);
}

sendButton.addEventListener('click', () => {
  const message = messageInput.value;
  if (message.trim() !== '') {
    addMessage(message, true); // Add user's message
    // Simulate a response (replace with actual server communication)
    setTimeout(() => {
      addMessage('Bot: ' + message, false); // Simulate a bot response
    }, 500);
    messageInput.value = '';
  }
});