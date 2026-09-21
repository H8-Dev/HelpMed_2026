/**
 * Global App State
 */
let currentProfile = localStorage.getItem("profile"); // 'DOCTOR' or 'PATIENT'
let activeChatId = null;
let useRealFlaskBackend = false; // Auto-detected or switched
const FLASK_API_BASE = 'http://127.0.0.1:5000/chats';
/**
 * Fallback In-Memory Mock Flask Database & Backend Simulation
 */
const mockDatabase = {
    doctor_chats: [
        {
            id: 'doc_pat_1',
            name: 'João Silva',
            avatar: 'P',
            avatarClass: '',
            messages: [
                { sender: 'IA', avatar: 'IA', type: 'ia', text: 'Resumo inicial da IA: Paciente relata dores na região lombar há 3 dias.' },
                { sender: 'P', avatar: 'P', type: 'patient', text: 'Doutor, a dor piora quando fico muito tempo sentado.' },
                { sender: 'M', avatar: 'M', type: 'doctor_sent', text: 'Olá João, recomendo repouso e manter a postura. Prescrevi um analgésico leve.' }
            ]
        },
        {
            id: 'doc_pat_2',
            name: 'Maria Oliveira',
            avatar: 'P',
            avatarClass: '',
            messages: [
                { sender: 'IA', avatar: 'IA', type: 'ia', text: 'Resumo inicial da IA: Retorno pré-operatório registrado com exames anexados.' },
                { sender: 'P', avatar: 'P', type: 'patient', text: 'Enviei os exames de sangue atualizados, aguardo avaliação.' }
            ]
        },
        {
            id: 'doc_pat_3',
            name: 'Carlos Souza',
            avatar: 'P',
            avatarClass: '',
            messages: [
                { sender: 'IA', avatar: 'IA', type: 'ia', text: 'Resumo inicial da IA: Dúvidas quanto à dosagem da medicação.' },
                { sender: 'P', avatar: 'P', type: 'patient', text: 'Boa tarde, devo tomar o remédio antes ou depois das refeições?' }
            ]
        }
    ],
    patient_chats: [
        {
            id: 'pat_ia',
            name: 'Atendente Virtual - HelpMed',
            avatar: 'IA',
            avatarClass: 'ia-avatar',
            messages: [
                { 
                    sender: 'IA', 
                    avatar: 'IA', 
                    type: 'info_card', 
                    text: 'A atendente virtual da HelpMed pode enviar diferentes mensagens, entre elas: Lembretes sobre agendamento, oferecer a opção de pagar suas consultas, informar seus problemas para que a IA encontre um médico apropriado e fazer perguntas sobre os problemas do paciente para enviar diretamente para o médico que irá atendê-lo.' 
                },
                { sender: 'IA', avatar: 'IA', type: 'ia', text: 'Olá! Como posso te ajudar hoje? Caso esteja sentindo algum sintoma, me descreva abaixo para eu direcionar ao médico especialista ideal.' },
                { sender: 'P', avatar: 'P', type: 'patient_sent', text: 'Olá, estou sentindo dores de cabeça frequentes desde ontem.' }
            ]
        },
        {
            id: 'pat_doc_1',
            name: 'Dr. Roberto Andrade',
            avatar: 'D',
            avatarClass: 'doctor-avatar',
            messages: [
                { sender: 'M', avatar: 'D', type: 'doctor', text: 'Olá! Como está evoluindo com o tratamento prescrito?' },
                { sender: 'P', avatar: 'P', type: 'patient_sent', text: 'Sinto melhoras significativas nas dores das articulações, Doutor!' }
            ]
        },
        {
            id: 'pat_doc_2',
            name: 'Dra. Camila Silva',
            avatar: 'D',
            avatarClass: 'doctor-avatar',
            messages: [
                { sender: 'M', avatar: 'D', type: 'doctor', text: 'Seus exames de rotina estão excelentes. Mantemos o retorno para daqui a 6 meses.' }
            ]
        }
    ]
};

/**
 * API Client Service (Flask Bridge with Automatic Fallback)
 */
const ApiService = {

    async fetchConversations() {
        if (useRealFlaskBackend) {
            try {
                const res = await fetch(`${FLASK_API_BASE}/${parseInt(localStorage.getItem("id").replace(/[^0-9]/g, ""))}`, { method: 'GET' });
                if (res.ok) return await res.json();
            } catch (err) {
                console.warn("Flask Backend unavailable, using local mock API persistence.");
                useRealFlaskBackend = false;
                document.getElementById('backend-status').textContent = 'API: Mock Local';
            }
        }
        
        // Fallback Mock API simulation
        return roleParam === 'doctor' ? mockDatabase.doctor_chats : mockDatabase.patient_chats;
    },

    async fetchMessages(chatId) {
        if (useRealFlaskBackend) {
            try {
                const res = await fetch(`${FLASK_API_BASE}/messages/${chatId}`);
                if (res.ok) return await res.json();
            } catch (err) {
                console.warn("Error fetching from Flask Backend.");
            }
        }
        // Fallback Mock search
        const allChats = [...mockDatabase.doctor_chats, ...mockDatabase.patient_chats];
        const found = allChats.find(c => c.id === chatId);
        return found ? found.messages : [];
    },

    async postMessage(chatId, messageObj) {
        if (useRealFlaskBackend) {
            try {
                const res = await fetch(`${FLASK_API_BASE}/messages`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chatId, message: messageObj })
                });
                if (res.ok) return await res.json();
            } catch (err) {
                console.warn("Failed posting message to Flask server.");
            }
        }
        // Fallback Mock Persistence
        const allChats = [...mockDatabase.doctor_chats, ...mockDatabase.patient_chats];
        const found = allChats.find(c => c.id === chatId);
        if (found) {
            found.messages.push(messageObj);
            saveMockStateToStorage();
            return { success: true, messages: found.messages };
        }
        return { success: false };
    }
};

function saveMockStateToStorage() {
    try {
        localStorage.setItem('helpmed_mock_db', JSON.stringify(mockDatabase));
    } catch (e) {
        console.error('LocalStorage write error:', e);
    }
}

function loadMockStateFromStorage() {
    try {
        const saved = localStorage.getItem('helpmed_mock_db');
        if (saved) {
            const parsed = JSON.parse(saved);
            if (parsed.doctor_chats && parsed.patient_chats) {
                mockDatabase.doctor_chats = parsed.doctor_chats;
                mockDatabase.patient_chats = parsed.patient_chats;
            }
        }
    } catch (e) {
        console.error('LocalStorage read error:', e);
    }
}

async function applyProfileUI() {
    const btnText = document.getElementById('profile-btn-text');
    const avatarBottom = document.getElementById('user-avatar-bottom');
    const navForms = document.getElementById('nav-forms');
    const navAi = document.getElementById('nav-ai');
    const labPerfil = document.getElementById('profile-label');
    if (currentProfile === 'DOCTOR') {
        labPerfil.textContent = 'Perfil Ativo: Médico';
        btnText.textContent = 'Alternar para Paciente';
        avatarBottom.textContent = 'M';
        avatarBottom.style.backgroundColor = 'var(--avatar-doctor-bg)';
        navForms.style.display = 'flex';
        navAi.style.display = 'flex';
    } else {
        labPerfil.textContent = 'Perfil Ativo: Paciente';
        btnText.textContent = 'Alternar para Médico';
        avatarBottom.textContent = 'P';
        avatarBottom.style.backgroundColor = 'var(--avatar-patient-bg)';
        navForms.style.display = 'none';
        navAi.style.display = 'none';
    }
    // Load updated conversation list dynamically for selected profile view
    await renderConversationsList();
}

async function renderConversationsList() {
    const listEl = document.getElementById('conversations-list');
    listEl.innerHTML = '';
    const availableChats = await ApiService.fetchConversations();
    if (availableChats && availableChats.length > 0) {

        // Ensure active Chat ID is valid for current view
        const isValidActive = availableChats.some(c => c.id === activeChatId);
        if (!isValidActive) {
            activeChatId = availableChats[0].id;
        }
    } else {
        activeChatId = null;
    }

    availableChats.forEach(chat => {
        const li = document.createElement('li');
        li.className = `patient-item ${chat.id === activeChatId ? 'active' : ''}`;
        li.onclick = () => selectChat(chat.id);
        const lastMsgObj = chat.messages && chat.messages.length > 0 ? chat.messages[chat.messages.length - 1] : null;
        const lastMsgText = lastMsgObj ? lastMsgObj.text : '';
        li.innerHTML = `
            <div class="patient-avatar ${chat.avatarClass || ''}">${chat.avatar}</div>
            <div class="patient-info">
                <span class="patient-name">${chat.name}</span>
                <span class="patient-last-msg">${lastMsgText}</span>
            </div>
        `;
        listEl.appendChild(li);
    });
    await renderActiveChat();
}

async function selectChat(chatId) {
    if (activeChatId === chatId) return;
    activeChatId = chatId;
    await renderConversationsList();
}

async function renderActiveChat() {
    if (!activeChatId) return;
    const chats = await ApiService.fetchConversations();
    const chat = chats.find(c => c.id === activeChatId);
    if (!chat) return;

    // Header Elements update

    const headerAvatar = document.getElementById('chat-header-avatar');
    const headerName = document.getElementById('chat-header-name');
    headerAvatar.className = `chat-patient-avatar ${chat.avatarClass || ''}`;
    headerAvatar.textContent = chat.avatar;
    headerName.textContent = chat.name;

    // Messages Container update

    const messagesContainer = document.getElementById('chat-messages-container');
    messagesContainer.innerHTML = '';

    // Fetch dynamic chat messages from backend/API
    
    const messages = await ApiService.fetchMessages(activeChatId);

    // Render Messages
    messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        if (msg.type === 'info_card') {
            msgDiv.className = 'message ia-message';
            msgDiv.innerHTML = `
                <div class="message-avatar ia-avatar">IA</div>
                <div class="info-card-bubble">${msg.text}</div>
            `;
        } else if (msg.type === 'ia') {
            msgDiv.className = 'message ia-message';
            msgDiv.innerHTML = `
                <div class="message-avatar ia-avatar">IA</div>
                <div class="message-bubble ia-bubble">${msg.text}</div>
            `;
        } else if (msg.type === 'patient') {
            msgDiv.className = 'message patient-message';
            msgDiv.innerHTML = `
                <div class="message-avatar">P</div>
                <div class="message-bubble patient-bubble">${msg.text}</div>
            `;
        } else if (msg.type === 'doctor') {
            msgDiv.className = 'message patient-message';
            msgDiv.innerHTML = `
                <div class="message-avatar doctor-avatar">D</div>
                <div class="message-bubble ia-bubble">${msg.text}</div>
            `;
        } else if (msg.type === 'doctor_sent') {
            msgDiv.className = 'message sent-message';
            msgDiv.innerHTML = `
                <div class="message-avatar doctor-avatar">M</div>
                <div class="message-bubble doctor-sent-bubble">${msg.text}</div>
            `;
        } else if (msg.type === 'patient_sent') {
            msgDiv.className = 'message sent-message';
            msgDiv.innerHTML = `
                <div class="message-avatar">P</div>
                <div class="message-bubble patient-sent-bubble">${msg.text}</div>
            `;
        }
        messagesContainer.appendChild(msgDiv);
    });
    // Auto-scroll to latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
function handleKeyPress(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}
async function sendMessage() {
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    if (!text || !activeChatId) return;
    const newMessageObj = currentProfile === 'DOCTOR' ? {
        sender: 'M',
        avatar: 'M',
        type: 'doctor_sent',
        text: text
    } : {
        sender: 'P',
        avatar: 'P',
        type: 'patient_sent',
        text: text
    };
    input.value = '';
    // Send to Flask API backend (or mock fallback)
    await ApiService.postMessage(activeChatId, newMessageObj);
    // Refresh UI dynamically without reloading screen
    await renderConversationsList();
    // Auto-trigger virtual assistant response if chatting with AI as Patient
    if (currentProfile === 'PATIENT' && activeChatId === 'pat_ia') {
        setTimeout(async () => {
            const aiReply = {
                sender: 'IA',
                avatar: 'IA',
                type: 'ia',
                text: 'Entendido. Registrei suas informações no seu prontuário e estou encaminhando para a equipe médica responsável.'
            };
            await ApiService.postMessage(activeChatId, aiReply);
            await renderConversationsList();
        }, 1000);
    }
}
/**
 * Initialization Procedure
 */
window.onload = async function() {
    loadMockStateFromStorage();
    // Test if a real Flask backend server is alive
    try {
        const res = await fetch(`${FLASK_API_BASE}/check`, { method: 'GET' });
        if (res.ok) {
            useRealFlaskBackend = true;
            document.getElementById('backend-status').textContent = 'API: Flask Conectada';
        }
    } catch (err) {
        // Flask not running locally, seamlessly fallback to Mock API persistence
        useRealFlaskBackend = false;
        document.getElementById('backend-status').textContent = 'API: Mock Local';
    }
    await applyProfileUI();
};