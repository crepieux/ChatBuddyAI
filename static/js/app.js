document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const newConversationBtn = document.getElementById('new-conversation-btn');
    const conversationList = document.getElementById('conversation-list');

    let currentConversationId = null;

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addMessage(sender, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = content;
        chatHistory.appendChild(messageElement);
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
                body: JSON.stringify({ message, conversation_id: currentConversationId }),
            })
            .then(response => response.json())
            .then(data => {
                addMessage('ai', data.ai_response);
                currentConversationId = data.conversation_id;
                updateConversationList();
            })
            .catch(error => console.error('Error:', error));
        }
    }

    function loadChatHistory(conversationId = null) {
        loadingSpinner.style.display = 'block';
        chatHistory.innerHTML = '';
        
        fetch(`/get_chat_history${conversationId ? '?conversation_id=' + conversationId : ''}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(message => {
                    addMessage(message.sender, message.content);
                });
                currentConversationId = data.length > 0 ? data[0].conversation_id : null;
            })
            .catch(error => console.error('Error:', error))
            .finally(() => {
                loadingSpinner.style.display = 'none';
            });
    }

    function updateConversationList() {
        fetch('/get_conversations')
            .then(response => response.json())
            .then(conversations => {
                conversationList.innerHTML = '';
                conversations.forEach(conv => {
                    const li = document.createElement('li');
                    li.textContent = `Conversation ${conv.id}`;
                    li.onclick = () => loadChatHistory(conv.id);
                    conversationList.appendChild(li);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    function startNewConversation() {
        currentConversationId = null;
        chatHistory.innerHTML = '';
        updateConversationList();
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    newConversationBtn.addEventListener('click', startNewConversation);

    // Initial load
    loadChatHistory();
    updateConversationList();
});
