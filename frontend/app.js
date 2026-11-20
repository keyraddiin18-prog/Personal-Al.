// =============================================
// KEYRADDIIN PERSONAL AI V2.0
// FRONTEND + BACKEND CONNECTION
// =============================================


// API CONFIGURATION
const API_BASE_URL = "YOUR_RENDER_BACKEND_URL";


// HTML ELEMENTS
const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");


// LOCAL STORAGE KEYS
const HISTORY_KEY = "keyraddiin_chat_history";
const CHAT_ID_KEY = "keyraddiin_chat_id";


// CHAT DATA
let chatHistory = [];

let currentChatId =
    localStorage.getItem(CHAT_ID_KEY) || null;


// =============================================
// LOAD SAVED CHAT HISTORY
// =============================================

function loadHistory() {

    try {

        const saved = localStorage.getItem(HISTORY_KEY);

        chatHistory = saved ? JSON.parse(saved) : [];

        if (!Array.isArray(chatHistory)) {
            chatHistory = [];
        }

        chatArea.innerHTML = "";

        if (chatHistory.length === 0) {
            showWelcome();
            return;
        }

        chatHistory.forEach(message => {

            addMessage(
                message.content,
                message.role === "user" ? "user" : "ai"
            );

        });

    } catch (error) {

        console.error("History loading error:", error);

        chatHistory = [];

        showWelcome();

    }

}


// =============================================
// SEND MESSAGE TO BACKEND
// =============================================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) return;

    if (
        API_BASE_URL === "YOUR_RENDER_BACKEND_URL" ||
        !API_BASE_URL
    ) {

        addMessage(
            "Backend URL is not configured yet. Please wait for deployment.",
            "ai"
        );

        return;

    }


    // Remove welcome screen
    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    // Display user message
    addMessage(message, "user");


    // Save user message locally
    chatHistory.push({
        role: "user",
        content: message
    });

    saveHistory();


    // Clear input
    userInput.value = "";

    userInput.disabled = true;

    if (sendBtn) {
        sendBtn.disabled = true;
    }


    // Loading message
    const loading = addMessage(
        "KEYRADDIIN AI is thinking...",
        "ai"
    );


    try {

        // CONNECT TO BACKEND
        const response = await fetch(
            `${API_BASE_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    message: message,

                    chat_id: currentChatId
                        ? Number(currentChatId)
                        : null

                })

            }
        );


        const data = await response.json();


        loading.remove();


        // CHECK RESPONSE
        if (!response.ok || !data.success) {

            throw new Error(
                data.detail ||
                data.error ||
                "AI request failed."
            );

        }


        // SAVE CHAT ID
        if (data.chat_id) {

            currentChatId = String(data.chat_id);

            localStorage.setItem(
                CHAT_ID_KEY,
                currentChatId
            );

        }


        // GET AI RESPONSE
        const aiResponse = data.response ||
            "I could not generate a response.";


        // DISPLAY AI RESPONSE
        addMessage(aiResponse, "ai");


        // SAVE AI RESPONSE
        chatHistory.push({

            role: "assistant",

            content: aiResponse

        });

        saveHistory();


    } catch (error) {

        loading.remove();

        console.error("CHAT ERROR:", error);


        addMessage(
            "Connection error: " +
            error.message +
            "\nPlease try again.",
            "ai"
        );

    } finally {

        userInput.disabled = false;

        if (sendBtn) {
            sendBtn.disabled = false;
        }

        userInput.focus();

    }

}


// =============================================
// DISPLAY MESSAGE
// =============================================

function addMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.style.maxWidth = "750px";

    messageDiv.style.margin = "20px auto";

    messageDiv.style.padding = "16px";

    messageDiv.style.borderRadius = "14px";

    messageDiv.style.lineHeight = "1.7";

    messageDiv.style.fontSize = "14px";

    messageDiv.style.whiteSpace = "pre-wrap";

    messageDiv.style.overflowWrap = "anywhere";


    if (sender === "user") {

        messageDiv.style.background = "#172c50";

        messageDiv.style.border = "1px solid #315b99";

    } else {

        messageDiv.style.background = "#111b31";

        messageDiv.style.border = "1px solid #263957";

    }


    messageDiv.textContent = text;

    chatArea.appendChild(messageDiv);

    chatArea.scrollTop = chatArea.scrollHeight;

    return messageDiv;

}


// =============================================
// SAVE HISTORY
// =============================================

function saveHistory() {

    localStorage.setItem(

        HISTORY_KEY,

        JSON.stringify(chatHistory)

    );

}


// =============================================
// NEW CHAT
// =============================================

function newChat() {

    chatHistory = [];

    currentChatId = null;


    localStorage.removeItem(HISTORY_KEY);

    localStorage.removeItem(CHAT_ID_KEY);


    showWelcome();

}


// =============================================
// WELCOME SCREEN
// =============================================

function showWelcome() {

    chatArea.innerHTML = `

        <div class="welcome">

            <div class="ai-icon">✦</div>

            <h1>Hello! Welcome to KEYRADDIIN AI.</h1>

            <p>Your personal intelligent assistant.</p>

        </div>

    `;

}


// =============================================
// SUGGESTION BUTTON
// =============================================

function suggest(message) {

    userInput.value = message;

    sendMessage();

}


// =============================================
// ENTER TO SEND
// =============================================

userInput.addEventListener("keydown", function(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

});


// =============================================
// SEND BUTTON
// =============================================

if (
    sendBtn &&
    !sendBtn.hasAttribute("onclick")
) {

    sendBtn.addEventListener(
        "click",
        sendMessage
    );

}


// =============================================
// INITIALIZE APP
// =============================================

loadHistory();


console.log(
    "KEYRADDIIN PERSONAL AI V2.0 Connected Frontend Loaded!"
);