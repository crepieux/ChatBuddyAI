document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.querySelector('.chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addMessage(sender, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = content;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage('user', message);
            messageInput.value = '';

            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            })
            .then(response => response.json())
            .then(data => {
                addMessage('ai', data.ai_response);
            })
            .catch(error => console.error('Error:', error));
        }
    }

    function loadChatHistory() {
        fetch('/get_chat_history')
            .then(response => response.json())
            .then(data => {
                chatMessages.innerHTML = '';
                data.forEach(message => {
                    addMessage(message.sender, message.content);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Load chat history when the page loads
    loadChatHistory();
});
