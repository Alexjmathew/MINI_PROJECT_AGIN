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
        
        // Create message content container
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Format code blocks if present
        if (!isUser && text.includes('```')) {
            const parts = text.split('```');
            let formatted = '';
            for (let i = 0; i < parts.length; i++) {
                if (i % 2 === 1) {
                    // Check if there's a language specified
                    const codeContent = parts[i].trim();
                    const firstLineBreak = codeContent.indexOf('\n');
                    
                    if (firstLineBreak > 0) {
                        const possibleLang = codeContent.substring(0, firstLineBreak).trim();
                        // If first line is a language name
                        if (possibleLang && !possibleLang.includes(' ')) {
                            const code = codeContent.substring(firstLineBreak + 1);
                            formatted += `<pre><code class="language-${possibleLang}">${code}</code></pre>`;
                        } else {
                            formatted += `<pre><code>${codeContent}</code></pre>`;
                        }
                    } else {
                        formatted += `<pre><code>${codeContent}</code></pre>`;
                    }
                } else {
                    formatted += parts[i].replace(/\n/g, '<br>');
                }
            }
            contentDiv.innerHTML = formatted;
        } else {
            contentDiv.innerHTML = text.replace(/\n/g, '<br>');
        }
        
        messageDiv.appendChild(contentDiv);

        // Add message metadata
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';
        
        // Add timestamp
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = 'Just now';
        metaDiv.appendChild(timeSpan);
        
        // Add source if provided
        if (source && !isUser) {
            const sourceSpan = document.createElement('span');
            sourceSpan.className = 'message-source';
            sourceSpan.textContent = `via ${source}`;
            metaDiv.appendChild(sourceSpan);
        }
        
        messageDiv.appendChild(metaDiv);
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
                addMessage(`Error: ${data.error}`, false, 'error');
            } else {
                addMessage(data.response, false, data.source);
            }
        } catch (error) {
            addMessage(`Error: ${error.message}`, false, 'error');
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
