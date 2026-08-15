// FinBot chat UI: sends messages to the backend API and renders bubbles with a typing animation
document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatMessages = document.getElementById("chatMessages");
    const suggestedChips = document.querySelectorAll(".fs-suggested-chip");

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    function appendUserMessage(text) {
        const msg = document.createElement("div");
        msg.className = "fs-msg fs-msg-user";
        msg.innerHTML = `
            <div class="fs-msg-bubble">${escapeHtml(text)}</div>
            <div class="fs-msg-avatar"><i class="bi bi-person-fill"></i></div>
        `;
        chatMessages.appendChild(msg);
        scrollToBottom();
    }

    function appendBotMessage(text) {
        const msg = document.createElement("div");
        msg.className = "fs-msg fs-msg-bot";
        msg.innerHTML = `
            <div class="fs-msg-avatar"><i class="bi bi-robot"></i></div>
            <div class="fs-msg-bubble">${escapeHtml(text)}</div>
        `;
        chatMessages.appendChild(msg);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typing = document.createElement("div");
        typing.className = "fs-msg fs-msg-bot fs-typing-indicator";
        typing.id = "typingIndicator";
        typing.innerHTML = `
            <div class="fs-msg-avatar"><i class="bi bi-robot"></i></div>
            <div class="fs-msg-bubble">
                <span class="fs-typing-dot"></span>
                <span class="fs-typing-dot"></span>
                <span class="fs-typing-dot"></span>
            </div>
        `;
        chatMessages.appendChild(typing);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const typing = document.getElementById("typingIndicator");
        if (typing) typing.remove();
    }

    async function sendMessage(message) {
        if (!message.trim()) return;
        appendUserMessage(message);
        chatInput.value = "";
        showTypingIndicator();

        try {
            const response = await fetch(CHAT_API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            removeTypingIndicator();

            if (response.ok && data.answer) {
                appendBotMessage(data.answer);
            } else {
                appendBotMessage("Sorry, something went wrong. Please try asking again.");
            }
        } catch (err) {
            removeTypingIndicator();
            appendBotMessage("I'm having trouble connecting right now. Please try again in a moment.");
        }
    }

    if (chatForm) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            sendMessage(chatInput.value);
        });
    }

    suggestedChips.forEach((chip) => {
        chip.addEventListener("click", () => {
            sendMessage(chip.dataset.question);
        });
    });

    scrollToBottom();
});
