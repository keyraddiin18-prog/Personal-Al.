// =============================================
// KEYRADDIIN PERSONAL AI V2.0
// COMPLETE FRONTEND CHAT SYSTEM
// Compatible with frontend/index.html
// =============================================


// =============================================
// API CONFIGURATION
// =============================================

const API_BASE_URL =
    "https://keyraddiin-personal-ai-nemg.onrender.com";


// =============================================
// HTML ELEMENTS
// =============================================

const chatArea = document.getElementById("chatSection");

const userInput = document.getElementById("userInput");

const sendBtn = document.getElementById("sendBtn");


// =============================================
// LOCAL STORAGE
// =============================================

const HISTORY_KEY = "keyraddiin_chat_history";

const CHAT_ID_KEY = "keyraddiin_chat_id";


// =============================================
// CHAT DATA
// =============================================

let chatHistory = [];

let currentChatId =
    localStorage.getItem(CHAT_ID_KEY) || null;


// =============================================
// CHECK HTML ELEMENTS
// =============================================

if (!chatArea || !userInput || !sendBtn) {

    console.error(
        "KEYRADDIIN AI ERROR: Required HTML elements not found."
    );

}


// =============================================
// LOAD CHAT HISTORY
// =============================================

function loadHistory() {

    try {

        const saved = localStorage.getItem(HISTORY_KEY);

        chatHistory = saved ? JSON.parse(saved) : [];

        if (!Array.isArray(chatHistory)) {

            chatHistory = [];

        }

        if (chatHistory.length === 0) {

            return;

        }

        const welcome = chatArea.querySelector(".welcome");

        if (welcome) {

            welcome.remove();

        }

        chatHistory.forEach(message => {

            addMessage(
                message.content,
                message.role === "user" ? "user" : "ai"
            );

        });

    }

    catch (error) {

        console.error(
            "History loading error:",
            error
        );

        chatHistory = [];

    }

}


// =============================================
// SEND MESSAGE TO BACKEND
// =============================================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) return;


    if (!API_BASE_URL) {

        addMessage(
            "Backend URL is not configured.",
            "ai"
        );

        return;

    }


    // Prevent duplicate requests

    if (sendBtn.disabled) return;


    // Remove welcome screen

    const welcome = chatArea.querySelector(".welcome");

    if (welcome) {

        welcome.remove();

    }


    // Display user message

    addMessage(message, "user");


    // Save user message

    chatHistory.push({

        role: "user",

        content: message

    });

    saveHistory();


    // Clear input

    userInput.value = "";

    userInput.disabled = true;

    sendBtn.disabled = true;


    // Loading message

    const loading = addMessage(
        "KEYRADDIIN AI is thinking...",
        "ai"
    );


    try {

        // Send request

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


        // Remove loading message

        loading.remove();


        // Check response

        if (!response.ok || !data.success) {

            throw new Error(

                data.detail ||
                data.error ||
                "AI request failed."

            );

        }


        // Save chat ID

        if (data.chat_id) {

            currentChatId = String(data.chat_id);

            localStorage.setItem(
                CHAT_ID_KEY,
                currentChatId
            );

        }


        // Get AI response

        const aiResponse =
            data.response ||
            "I could not generate a response.";


        // Display AI response

        addMessage(aiResponse, "ai");


        // Save AI response

        chatHistory.push({

            role: "assistant",

            content: aiResponse

        });

        saveHistory();


    }

    catch (error) {

        loading.remove();

        console.error(
            "CHAT ERROR:",
            error
        );


        addMessage(

            "Connection error: " +
            error.message +
            "\nPlease try again.",

            "ai"

        );

    }

    finally {

        userInput.disabled = false;

        sendBtn.disabled = false;

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

        messageDiv.style.border =
            "1px solid #315b99";

        messageDiv.style.marginLeft = "auto";

    }

    else {

        messageDiv.style.background = "#111b31";

        messageDiv.style.border =
            "1px solid #263957";

        messageDiv.style.marginRight = "auto";

    }


    messageDiv.textContent = text;

    chatArea.appendChild(messageDiv);

    chatArea.scrollTop = chatArea.scrollHeight;


    return messageDiv;

}


// =============================================
// SAVE CHAT HISTORY
// =============================================

function saveHistory() {

    try {

        localStorage.setItem(

            HISTORY_KEY,

            JSON.stringify(chatHistory)

        );

    }

    catch (error) {

        console.error(
            "Could not save chat history:",
            error
        );

    }

}


// =============================================
// NEW CHAT
// =============================================

function newChat() {

    chatHistory = [];

    currentChatId = null;


    localStorage.removeItem(HISTORY_KEY);

    localStorage.removeItem(CHAT_ID_KEY);


    chatArea.innerHTML = "";

    showWelcome();

}


// =============================================
// WELCOME SCREEN
// =============================================

function showWelcome() {

    chatArea.innerHTML = `

        <div class="welcome">

            <div class="ai-icon">✦</div>

            <h1>
                Hello! Welcome to KEYRADDIIN AI.
            </h1>

            <p>
                Your personal intelligent assistant.
                Ask me anything and let's explore
                knowledge together.
            </p>

            <div class="suggestions">

                <button onclick="suggest('Explain science to me')">
                    🔬 Explain Science
                </button>

                <button onclick="suggest('Help me study Grade 10')">
                    📚 Study Assistant
                </button>

                <button onclick="suggest('Translate English to Afaan Oromo')">
                    🌍 Translation
                </button>

            </div>

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

userInput.addEventListener(

    "keydown",

    function(event) {

        if (

            event.key === "Enter" &&
            !event.shiftKey

        ) {

            event.preventDefault();

            sendMessage();

        }

    }

);


// =============================================
// INITIALIZE APPLICATION
// =============================================

loadHistory();


console.log(
    "KEYRADDIIN PERSONAL AI V2.0 READY!"
);