// =============================================
// KEYRADDIIN PERSONAL AI V2.0
// PROFESSIONAL FRONTEND CHAT SYSTEM
// =============================================


// =============================================
// API CONFIGURATION
// =============================================

const API_BASE_URL =
    "https://keyraddiin-personal-ai-v2.onrender.com";


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
// API REQUEST HELPER
// =============================================

async function apiRequest(endpoint, options = {}) {

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        options
    );

    const contentType =
        response.headers.get("content-type") || "";

    let data;

    if (contentType.includes("application/json")) {
        data = await response.json();
    } else {
        data = {
            detail: await response.text()
        };
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.error ||
            `Server error: ${response.status}`
        );

    }

    return data;

}


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

            if (!message || typeof message.content !== "string") {
                return;
            }

            addMessage(
                message.content,
                message.role === "user" ? "user" : "ai"
            );

        });

    } catch (error) {

        console.error("History loading error:", error);

        chatHistory = [];

    }

}


// =============================================
// SEND MESSAGE TO BACKEND
// =============================================

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) return;

    if (sendBtn.disabled) return;


    if (!API_BASE_URL) {

        addMessage(
            "Backend URL is not configured.",
            "ai"
        );

        return;

    }


    const welcome = chatArea.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    // DISPLAY USER MESSAGE

    addMessage(message, "user");


    // SAVE USER MESSAGE

    chatHistory.push({

        role: "user",

        content: message

    });

    saveHistory();


    // CLEAR INPUT

    userInput.value = "";

    userInput.disabled = true;

    sendBtn.disabled = true;


    // LOADING MESSAGE

    const loading = addMessage(
        "KEYRADDIIN AI is thinking...",
        "ai"
    );


    try {

        // SEND REQUEST TO BACKEND

        const data = await apiRequest(
            "/chat",
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


        // REMOVE LOADING

        loading.remove();


        // CHECK API RESPONSE

        if (!data.success) {

            throw new Error(
                data.error || "AI request failed."
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

        const aiResponse =
            data.response ||
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
            "\n\nPlease check your internet connection and try again.",

            "ai"

        );

    } finally {

        userInput.disabled = false;

        sendBtn.disabled = false;

        userInput.focus();

    }

}


// =============================================
// DISPLAY MESSAGE
// =============================================

function addMessage(text, sender) {

    const row = document.createElement("div");

    row.className =
        "message-row " +
        (sender === "user" ? "user" : "ai");


    const bubble = document.createElement("div");

    bubble.className = "message-bubble";


    const label = document.createElement("span");

    label.className = "message-label";

    label.textContent =
        sender === "user"
            ? "YOU"
            : "✦ KEYRADDIIN AI";


    const content = document.createElement("div");

    content.textContent = String(text);


    bubble.appendChild(label);

    bubble.appendChild(content);

    row.appendChild(bubble);

    chatArea.appendChild(row);


    chatArea.scrollTop = chatArea.scrollHeight;


    return row;

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

    } catch (error) {

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


    console.log("NEW CHAT STARTED");

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

console.log(
    "BACKEND:",
    API_BASE_URL
);