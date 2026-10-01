/**
 * app.js - Frontend Controller for OWASP AI Flaw Machine
 */

let challengesData = {};
let currentChallengeId = "level_1_prompt_leak";
let userScore = 0;

// DOM Elements
const challengeListEl = document.getElementById("challenge-list");
const chatContainer = document.getElementById("chat-container");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const flagForm = document.getElementById("flag-form");
const flagInput = document.getElementById("flag-input");
const flagResultToast = document.getElementById("flag-result-toast");

// Header elements
const activeTitle = document.getElementById("active-title");
const activeDesc = document.getElementById("active-desc");
const activeDifficulty = document.getElementById("active-difficulty");
const activeCategory = document.getElementById("active-category");
const activePoints = document.getElementById("active-points");
const userScoreEl = document.getElementById("user-score");
const solvedCountEl = document.getElementById("solved-count");

// Inspector elements
const xrayPrompt = document.getElementById("xray-prompt");
const telemetryTime = document.getElementById("telemetry-time");
const chipTokens = document.getElementById("chip-tokens");
const sandboxFiles = document.getElementById("sandbox-files");
const sandboxDb = document.getElementById("sandbox-db");
const hintsContainer = document.getElementById("hints-container");

// ==========================================
// Initialization
// ==========================================

async function init() {
    setupTabs();
    setupEventListeners();
    await loadChallenges();
    await loadSandbox();
}

// Tab Switching
function setupTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const targetId = `tab-${btn.dataset.tab}`;
            const targetContent = document.getElementById(targetId);
            if (targetContent) targetContent.classList.add("active");

            if (btn.dataset.tab === "sandbox") {
                loadSandbox();
            }
        });
    });
}

// Event Listeners
function setupEventListeners() {
    chatForm.addEventListener("submit", handleSendMessage);
    flagForm.addEventListener("submit", handleFlagSubmission);
}

// ==========================================
// Challenges Loading & Selection
// ==========================================

async function loadChallenges() {
    try {
        const res = await fetch("/api/levels");
        challengesData = await res.json();
        renderChallengeList();
        selectChallenge(currentChallengeId);
    } catch (e) {
        console.error("Failed to load challenges:", e);
    }
}

function renderChallengeList() {
    challengeListEl.innerHTML = "";
    let solvedCount = 0;
    userScore = 0;

    Object.values(challengesData).forEach(ch => {
        if (ch.solved) {
            solvedCount++;
            userScore += ch.points;
        }

        const card = document.createElement("div");
        card.className = `challenge-card ${ch.id === currentChallengeId ? 'active' : ''} ${ch.solved ? 'solved' : ''}`;
        card.innerHTML = `
            <div class="challenge-card-title">${ch.solved ? '[SOLVED] ' : ''}${ch.title}</div>
            <div class="card-meta">
                <span>${ch.difficulty}</span>
                <span>+${ch.points} PTS</span>
            </div>
        `;
        card.onclick = () => selectChallenge(ch.id);
        challengeListEl.appendChild(card);
    });

    userScoreEl.innerText = `${userScore} PTS`;
    solvedCountEl.innerText = `${solvedCount} / ${Object.keys(challengesData).length}`;
}

function selectChallenge(id) {
    currentChallengeId = id;
    const ch = challengesData[id];
    if (!ch) return;

    // Update Header
    activeTitle.innerText = ch.title;
    activeDesc.innerText = ch.description;
    activeDifficulty.innerText = ch.difficulty;
    activeCategory.innerText = ch.category;
    activePoints.innerText = `+${ch.points} PTS`;

    // Reset Chat Window for Challenge
    chatContainer.innerHTML = `
        <div class="chat-message bot-message">
            <div class="msg-avatar">BOT</div>
            <div class="msg-content">
                <strong>AI Assistant:</strong>
                <p>Mission loaded: <strong>${ch.title}</strong>. Send your prompt below.</p>
            </div>
        </div>
    `;

    // Render Hints
    hintsContainer.innerHTML = ch.hints.map((h, i) => `
        <div class="hint-item">
            <strong>Hint ${i + 1}:</strong> ${h}
        </div>
    `).join("");

    renderChallengeList();
}

// ==========================================
// Chat Submission & Telemetry Rendering
// ==========================================

async function handleSendMessage(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Append User Message to UI
    appendChatMessage("user", message);
    userInput.value = "";

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                challenge_id: currentChallengeId,
                message: message
            })
        });

        const data = await res.json();
        
        // Append Bot Reply to UI
        appendChatMessage("bot", data.reply);

        // Update X-Ray Telemetry
        updateXRayTelemetry(data.telemetry);

    } catch (err) {
        appendChatMessage("bot", "Error: Unable to reach AI agent server.");
        console.error(err);
    }
}

function appendChatMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-message ${role}-message`;
    msgDiv.innerHTML = `
        <div class="msg-avatar">${role === 'user' ? 'YOU' : 'BOT'}</div>
        <div class="msg-content">
            <strong>${role === 'user' ? 'You' : 'AI Assistant'}:</strong>
            <p>${formatMessageContent(text)}</p>
        </div>
    `;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function formatMessageContent(text) {
    return text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>').replace(/\n/g, '<br>');
}

// Update Live X-Ray Inspector Panel
function updateXRayTelemetry(t) {
    if (!t) return;

    telemetryTime.innerText = `${t.execution_time_ms} ms`;
    chipTokens.innerText = `~${t.token_estimate}`;
    xrayPrompt.innerText = t.system_prompt;
}

// ==========================================
// Flag Submission & Score Tracking
// ==========================================

async function handleFlagSubmission(e) {
    e.preventDefault();
    const flag = flagInput.value.trim();
    if (!flag) return;

    try {
        const res = await fetch("/api/flag", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                challenge_id: currentChallengeId,
                flag: flag
            })
        });

        const data = await res.json();
        flagResultToast.innerText = data.message;
        flagResultToast.style.color = data.correct ? "#00ff88" : "#ff3366";

        if (data.correct) {
            challengesData[currentChallengeId].solved = true;
            renderChallengeList();
            flagInput.value = "";
        }
    } catch (err) {
        console.error("Flag submission error:", err);
    }
}

// ==========================================
// Sandbox Viewer
// ==========================================

async function loadSandbox() {
    try {
        const res = await fetch("/api/sandbox");
        const data = await res.json();

        // Files
        sandboxFiles.innerHTML = data.files.map(f => `<div>[FILE] ${f}</div>`).join("");

        // Database Preview
        sandboxDb.innerHTML = `
            <div><strong>Products (${data.database_products.length} rows):</strong></div>
            <pre>${JSON.stringify(data.database_products, null, 2)}</pre>
        `;
    } catch (e) {
        console.error("Error loading sandbox:", e);
    }
}

// Launch on page load
window.addEventListener("DOMContentLoaded", init);
