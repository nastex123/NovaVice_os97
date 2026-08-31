document.addEventListener("DOMContentLoaded", () => {
    const chatHistory = document.getElementById("chat-history");
    const chatForm = document.getElementById("chat-form");
    const queryInput = document.getElementById("query-input");
    const voiceBtn = document.getElementById("voice-btn");
    const opencodeToggle = document.getElementById("opencode-toggle");
    const chipsContainer = document.getElementById("chips-container");

    // Telemetry fields
    const metricQueries = document.getElementById("metric-queries");
    const metricCache = document.getElementById("metric-cache");
    const metricEscalations = document.getElementById("metric-escalations");
    const metricCost = document.getElementById("metric-cost");

    let isRecording = false;
    let recognition = null;

    // Check Web Speech API support
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "es-ES";

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            queryInput.value = transcript;
            chatForm.dispatchEvent(new Event("submit"));
        };

        recognition.onend = () => {
            isRecording = false;
            voiceBtn.classList.remove("recording");
        };

        voiceBtn.addEventListener("click", () => {
            if (!isRecording) {
                recognition.start();
                isRecording = true;
                voiceBtn.classList.add("recording");
            } else {
                recognition.stop();
                isRecording = false;
                voiceBtn.classList.remove("recording");
            }
        });
    } else {
        voiceBtn.style.display = "none";
    }

    // Markdown Parser for structured bold, bullet points and headers
    function parseMarkdown(text) {
        if (!text) return "";
        let html = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Headers ###
        html = html.replace(/^### (.*$)/gim, '<h4 class="msg-heading">$1</h4>');
        html = html.replace(/^## (.*$)/gim, '<h3 class="msg-heading">$1</h3>');

        // Bold **text**
        html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

        // Italic *text*
        html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");

        // Bullet points
        html = html.replace(/^[•\-\*] (.*$)/gim, '<div class="msg-bullet"><span class="bullet-dot">•</span><span>$1</span></div>');

        // Line breaks
        html = html.replace(/\n/g, "<br>");

        return html;
    }

    // Send query helper
    function sendQuery(text) {
        queryInput.value = text;
        chatForm.dispatchEvent(new Event("submit"));
    }

    // Update bottom chips row dynamically based on action buttons
    function updateChips(actionButtons) {
        if (!chipsContainer) return;
        if (!actionButtons || actionButtons.length === 0) {
            actionButtons = [
                { label: "1. Carreras y Modalidades", value: "1" },
                { label: "2. Precios y Cuotas", value: "2" },
                { label: "3. Fechas Otoño 2026", value: "3" },
                { label: "4. Becas y Ayudas", value: "4" },
                { label: "5. Hablar con Asesor", value: "5" },
                { label: "0. Menú Principal", value: "0" }
            ];
        }

        chipsContainer.innerHTML = "";
        actionButtons.forEach(btn => {
            const b = document.createElement("button");
            b.className = "chip";
            b.textContent = btn.label;
            b.addEventListener("click", () => sendQuery(btn.value));
            chipsContainer.appendChild(b);
        });
    }

    // Append Message to History
    function appendMessage(text, isUser = false, metadata = null) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${isUser ? "user-msg" : "assistant-msg"}`;

        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = isUser ? "TÚ" : "NTU";

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";

        const contentDiv = document.createElement("div");
        contentDiv.className = "msg-content";
        contentDiv.innerHTML = parseMarkdown(text);
        bubble.appendChild(contentDiv);

        // Render inline interactive action buttons if provided
        if (metadata && metadata.action_buttons && metadata.action_buttons.length > 0) {
            const btnRow = document.createElement("div");
            btnRow.className = "inline-buttons-row";

            metadata.action_buttons.forEach(btn => {
                const actionBtn = document.createElement("button");
                actionBtn.className = "inline-action-btn";
                actionBtn.textContent = btn.label;
                actionBtn.addEventListener("click", () => sendQuery(btn.value));
                btnRow.appendChild(actionBtn);
            });

            bubble.appendChild(btnRow);
            updateChips(metadata.action_buttons);
        }

        if (metadata && !isUser) {
            const metaDiv = document.createElement("div");
            metaDiv.className = "msg-meta";

            if (metadata.confidence_score !== undefined) {
                const conf = document.createElement("span");
                conf.className = "meta-badge confidence";
                conf.textContent = `Confianza: ${(metadata.confidence_score * 100).toFixed(1)}%`;
                metaDiv.appendChild(conf);
            }

            if (metadata.cached) {
                const cacheBadge = document.createElement("span");
                cacheBadge.className = "meta-badge";
                cacheBadge.textContent = "Caché Activa";
                metaDiv.appendChild(cacheBadge);
            }

            if (metadata.latency_ms) {
                const latencyBadge = document.createElement("span");
                latencyBadge.className = "meta-badge";
                latencyBadge.textContent = `${metadata.latency_ms} ms`;
                metaDiv.appendChild(latencyBadge);
            }

            if (metadata.escalated_to_human) {
                const esc = document.createElement("span");
                esc.className = "meta-badge escalated";
                esc.textContent = `Escalado a Humano (${metadata.escalation_ticket_id || "Ticket Registrado"})`;
                metaDiv.appendChild(esc);
            }

            if (metadata.source_documents && metadata.source_documents.length > 0) {
                metadata.source_documents.forEach(src => {
                    const srcBadge = document.createElement("span");
                    srcBadge.className = "meta-badge source";
                    srcBadge.textContent = src;
                    metaDiv.appendChild(srcBadge);
                });
            }

            bubble.appendChild(metaDiv);
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // Submit Query
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        appendMessage(query, true);
        queryInput.value = "";

        const useOpenCode = opencodeToggle ? opencodeToggle.checked : false;
        let sessionId = localStorage.getItem("ntu_admissions_session");
        if (!sessionId) {
            sessionId = "web_session_" + Math.random().toString(36).substring(2, 9);
            localStorage.setItem("ntu_admissions_session", sessionId);
        }

        try {
            const res = await fetch("/api/v1/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: query,
                    user_id: "postulante_web",
                    session_id: sessionId,
                    use_opencode_mode: useOpenCode
                })
            });

            if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
            const data = await res.json();
            appendMessage(data.response, false, data);
            fetchMetrics();
        } catch (err) {
            appendMessage(`Error al contactar con el servidor de admisiones: ${err.message}`, false);
        }
    });

    // Handle Quick Chips
    document.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const q = chip.getAttribute("data-query");
            if (q) sendQuery(q);
        });
    });

    // Fetch Live Telemetry
    async function fetchMetrics() {
        try {
            const res = await fetch("/api/v1/metrics");
            if (res.ok) {
                const data = await res.json();
                if (metricQueries) metricQueries.textContent = data.total_queries_processed;
                if (metricCache) metricCache.textContent = `${(data.cache_hit_ratio * 100).toFixed(1)}%`;
                if (metricEscalations) metricEscalations.textContent = data.total_escalations;
                if (metricCost) metricCost.textContent = `$${data.estimated_total_cost_usd.toFixed(4)}`;
            }
        } catch (e) {
            // Silently ignore telemetry poll errors
        }
    }

    setInterval(fetchMetrics, 10000);
    fetchMetrics();
});
