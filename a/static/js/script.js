document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-button');
    const quickBtns = document.querySelectorAll('.quick-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    // Function to add message to chat
    function addMessage(text, isUser, source) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        // Format code blocks if present
        if (!isUser && text.includes('```')) {
            const parts = text.split('```');
            let formatted = '';
            for (let i = 0; i < parts.length; i++) {
                formatted += i % 2 === 1
                    ? `<pre><code>${parts[i]}</code></pre>`
                    : parts[i].replace(/\n/g, '<br>');
            }
            messageDiv.innerHTML = formatted;
        } else {
            messageDiv.innerHTML = text;
        }

        // Add source if provided
        if (source && !isUser) {
            const sourceSpan = document.createElement('span');
            sourceSpan.className = 'message-source';
            sourceSpan.textContent = ` (via ${source})`;
            messageDiv.appendChild(sourceSpan);
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send message
    async function sendMessage(message) {
        if (!message.trim()) return;

        // Show typing indicator
        typingIndicator.style.display = 'flex';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            if (data.error) {
                addMessage(`Error: ${data.error}`, false);
            } else {
                addMessage(data.response, false, data.source);
            }
        } catch (error) {
            // Fixed: Use error.message instead of undefined data.error
            addMessage(`Error: ${error.message}`, false);
        } finally {
            // Hide typing indicator
            typingIndicator.style.display = 'none';
        }
    }

    // Event Listeners
    sendBtn.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            sendMessage(message);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Quick button handlers
    quickBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            if (question) {
                addMessage(question, true);
                sendMessage(question);
            }
        });
    });
});
