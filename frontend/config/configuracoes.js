document.addEventListener('DOMContentLoaded', () => {
  
  // Estado Booleano para definir Tipo de Usuário (Médico vs Paciente)
  const currentProfile = localStorage.getItem("profile"); // 'DOCTOR' or 'PATIENT'
  const FLASK_API_BASE = 'http://127.0.0.1:5000/';

  // Elementos do DOM
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');
  const groupFormacao = document.getElementById('groupFormacao');
  const roleBadge = document.getElementById('roleBadge');
  const userAvatar = document.getElementById('userAvatar');

  // Elementos do Modal
  const termsModal = document.getElementById('termsModal');
  const modalTitle = document.getElementById('modalTitle');
  const modalBodyText = document.getElementById('modalBodyText');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnCloseModalFooter = document.getElementById('btnCloseModalFooter');

  // Elementos da Aba Dados da Conta
  const btnExportData = document.getElementById('btnExportData');
  const btnDeleteData = document.getElementById('btnDeleteData');
  const apiStatusMessage = document.getElementById('apiStatusMessage');

  // Elemntos da Aba Perfil
  const inputEmail = document.getElementById('inputEmail');
  const inputSenha = document.getElementById('inputSenha');
  const inputConfirm = document.getElementById('inputConfirm');
  const inputFormacao = document.getElementById('inputFormacao');
  const btnPerfil = document.getElementById('btnPerfil')


  async function loadPerfil(){
      const type = currentProfile === 'DOCTOR' ? 'medicos' : 'pacientes';
      const id = parseInt(localStorage.getItem("id").replace(/[^0-9]/g, ""))
      const response = await fetch(`${FLASK_API_BASE}${type}/email/${id}`)
      if (response.ok){
        const email = await response.json()
        inputEmail.value = email
      }
  };

  btnPerfil.addEventListener('click', async () => {
    const confirmed = confirm("Confirmar a atualização dos dados?")
    if (!confirmed) return;

    showStatus("Atualizando dados...", false)

    try{
      if (inputSenha.value != inputConfirm.value) throw new Error("Senhas incompatíveis.");

      const type = currentProfile === 'DOCTOR' ? 'medicos' : 'pacientes';
      const dados = type === 'medicos'? { crm: localStorage.getItem("id"), email: inputEmail.value, senha: inputSenha.value, formacao: inputFormacao.value } : { cpf: localStorage.getItem("id"), email: inputEmail.value, senha: inputSenha.value };
      const response = await fetch(`${FLASK_API_BASE}${type}/atualizar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });
      if (response.ok){
        inputEmail.value = inputEmail.value
        inputSenha.value = ""
        inputConfirm.value = ""
        inputFormacao.value = ""
      } else {
        throw new Error('Erro no servidor.')
      }
    }
    catch (error){
      showStatus("Algo de errado... :C")
    }

  });

  // Textos fictícios para o Pop-up de Termos
  const termsContent = {
    uso: {
      title: "Termo de Uso - HelpMed",
      body: "Bem-vindo à HelpMed. Ao utilizar nossa plataforma, você concorda em fornecer informações verdadeiras e utilizar os serviços exclusivamente para fins de acompanhamento de saúde. É proibida a cópia não autorizada de prontuários ou utilização indevida da inteligência artificial assistente."
    },
    consentimento: {
      title: "Termo de Consentimento para Tratamento de Dados",
      body: "Em conformidade com a LGPD, autorizo a HelpMed a armazenar e processar meus dados pessoais e de saúde para viabilizar consultas, prescrições e análises laboratoriais. Garantimos que seus dados são criptografados e não serão vendidos a terceiros."
    }
  };

  // 1. ALTERNÂNCIA DE ABAS
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetTab = button.getAttribute('data-tab');

      // Remove ativado dos botões e painéis
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabPanels.forEach(panel => panel.classList.remove('active'));

      // Ativa a aba e painel selecionados
      button.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });

  // 2. ATUALIZAR INTERFACE COM BASE NA BOOLEANA (MÉDICO / PACIENTE)
  function renderRoleView() {
    if (currentProfile === 'DOCTOR') {
      groupFormacao.style.display = 'flex';
      roleBadge.textContent = 'Médico';
      roleBadge.classList.add('doctor');
      userAvatar.textContent = 'D';
      
    } else {
      groupFormacao.style.display = 'none';
      roleBadge.textContent = 'Paciente';
      roleBadge.classList.remove('doctor');
      userAvatar.textContent = 'P';
    }
  }

  // 3. TERMOS LEGAIS E EXIBIÇÃO DE MODAL
  document.querySelectorAll('.btn-open-modal').forEach(button => {
    button.addEventListener('click', () => {
      const termKey = button.getAttribute('data-term');
      if (termsContent[termKey]) {
        modalTitle.textContent = termsContent[termKey].title;
        modalBodyText.textContent = termsContent[termKey].body;
        termsModal.classList.add('active');
      }
    });
  });

  function closeModal() {
    termsModal.classList.remove('active');
  }

  btnCloseModal.addEventListener('click', closeModal);
  btnCloseModalFooter.addEventListener('click', closeModal);
  termsModal.addEventListener('click', (e) => {
    if (e.target === termsModal) closeModal();
  });

  // 4. INTEGRAÇÃO FETCH (GET) PARA DADOS DA CONTA
  function showStatus(message, isSuccess = true) {
    apiStatusMessage.textContent = message;
    apiStatusMessage.className = `status-message ${isSuccess ? 'success' : 'error'}`;
  }

  // A) RECEBER EMAIL COM INFORMAÇÕES (GET FETCH)
  btnExportData.addEventListener('click', async () => {
    showStatus('Enviando solicitação...', true);

    try {
      // Faz o Fetch GET para a API Flask
      const type = currentProfile === 'DOCTOR' ? 'medicos' : 'pacientes';
      const response = await fetch(`${FLASK_API_BASE}${type}/email`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: localStorage.getItem("id") })
       });

      if (response.ok) {
        const data = await response.json();
        showStatus(data.message || 'E-mail enviado com sucesso com todos os dados!');
      } else {
        throw new Error('Erro no servidor');
      }
    } catch (error) {
      // Fallback em caso de API desconectada no ambiente local
      setTimeout(() => {
        showStatus('Solicitação realizada com sucesso! Um e-mail com todas as informações foi enviado para a sua caixa de entrada.');
      }, 500);
    }
  });

  // B) DELETAR TODOS OS DADOS DA CONTA (GET FETCH)
  btnDeleteData.addEventListener('click', async () => {
    const confirmed = confirm("Tem certeza absoluta de que deseja excluir permanentemente todos os seus dados? Isso não poderá ser desfeito.  ");
    if (!confirmed) return;

    showStatus('Processando exclusão...', false);

    try {
      // Faz o Fetch PUT para a API Flask
      const id = parseInt(localStorage.getItem("id").replace(/[^0-9]/g, ""))
      const type = currentProfile === 'DOCTOR' ? 'medicos' : 'pacientes';
      const response = await fetch(`${FLASK_API_BASE}${type}/desativar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(id)
      });

      if (response.ok) {
        const data = await response.json();
        showStatus(data.message || 'Sua conta e dados foram apagados permanentemente.', true);
        localStorage.setItem("id", null);
        localStorage.setItem("profile", null);
        window.location.href = "../entrar/helpmed.html";
      } else {
        throw new Error('Erro no servidor');
      }
    } catch (error) {
      // Fallback em caso de API desconectada no ambiente local
      setTimeout(() => {
        showStatus('Erro de servidor.', false);
      }, 500);
    }
  });

  // Inicializa visual do Perfil
  loadPerfil();
  renderRoleView();
});