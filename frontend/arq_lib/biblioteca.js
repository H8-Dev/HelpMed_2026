document.addEventListener('DOMContentLoaded', () => {
  const API_URL = 'http://127.0.0.1:5000/arquivos';
  const filesGrid = document.getElementById('filesGrid');
  const btnFloatingAdd = document.getElementById('btnFloatingAdd');
  const fileInput = document.getElementById('fileInput');
  const profile = localStorage.getItem("profile");


  // Elementos do Modal
  const modalFileId = document.getElementById('modalFileId');
  const fileModal = document.getElementById('fileModal');
  const modalBadge = document.getElementById('modalBadge');
  const modalFileName = document.getElementById('modalFileName');
  const modalSpinner = document.getElementById('modalSpinner');
  const modalTextContent = document.getElementById('modalTextContent');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnCloseModalFooter = document.getElementById('btnCloseModalFooter');
  const btnDownloadModal = document.getElementById('btnDownloadModal');


  // 1. CARREGAR LISTA DE ARQUIVOS (GET /api/files)
  async function loadLibrary() {
    try {
      const response = await fetch(`${API_URL}/usuario/${parseInt(localStorage.getItem("id").replace(/[^0-9]/g, ""))}`, { method: 'GET' });
      if (!response.ok) throw new Error('Servidor não disponível');
      const files = await response.json();
      renderGrid(files);
    } catch (err) {
      console.warn('API não conectada. Utilizando estado local.', err);
    }
  }

  // 2. RENDERIZAR MINIATURAS NO GRID
  function renderGrid(files) {
    filesGrid.innerHTML = '';

    files.forEach(file => {
      const card = document.createElement('div');
      card.className = 'file-card';
      
      
      const ext = file.name.split('.').pop().toLowerCase();
      const isDoc = ext === 'doc' || ext === 'docx' || file.type === 'doc';
      const badgeClass = isDoc ? 'doc' : 'pdf';
      const badgeText = isDoc ? 'DOC' : 'PDF';

      card.innerHTML = `
        <div class="file-thumbnail">
          <span class="file-badge ${badgeClass}">${badgeText}</span>
          <div class="doc-lines">
            <div class="doc-line full"></div>
            <div class="doc-line medium"></div>
            <div class="doc-line short"></div>
            <div class="doc-line full"></div>
          </div>
        </div>
        <span class="file-label" title="${file.name}">${file.name}</span>
      `;

      // Evento de clique para abrir conteúdo via Fetch
      card.addEventListener('click', () => fetchAndOpenFile(file.id, file.name, badgeText, badgeClass));

      filesGrid.appendChild(card);
    });
  }

  // 3. FETCH GET DO CONTEÚDO DO ARQUIVO E EXIBIÇÃO NO MODAL
  async function fetchAndOpenFile(id, name, badgeText, badgeClass) {
    // Configura o cabeçalho do Modal
    modalFileId.textContent = id;
    modalFileName.textContent = name;
    modalBadge.textContent = badgeText;
    modalBadge.className = `file-badge ${badgeClass}`;

    // Exibe o Spinner de Carregamento
    modalSpinner.style.display = 'flex';
    modalTextContent.style.display = 'none';
    fileModal.classList.add('active');

    try {
      // Requisição GET individual do arquivo
      const response = await fetch(`${API_URL}/${id}`);
      if (!response.ok) throw new Error('Erro ao buscar o arquivo');
      const data = await response.json();
      console.log('Conteúdo do arquivo recebido:', data);
      displayModalContent(data.content || 'Sem conteúdo disponível.');
    } catch (err) {
      console.warn('Erro ao buscar o arquivo:', err);
      displayModalContent('Erro ao carregar o conteúdo do arquivo.');
    }
  }

  function displayModalContent(text) {
    modalSpinner.style.display = 'none';
    modalTextContent.textContent = text;
    modalTextContent.style.display = 'block';
  }

  function convertorArquivos(file){
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64Content = reader.result.split(',')[1];
        resolve(base64Content);
      }
      reader.onerror = (error) => reject(error);
    });
  }

  // 4. FECHAR MODAL
  function closeModal() {
    fileModal.classList.remove('active');
  }

  btnCloseModal.addEventListener('click', closeModal);
  btnCloseModalFooter.addEventListener('click', closeModal);
  fileModal.addEventListener('click', (e) => {
    if (e.target === fileModal) closeModal();
  });

  btnDownloadModal.addEventListener('click', downloadFile);
  async function downloadFile(){
    const fileId = modalFileId.textContent;
    const response = await fetch(`${API_URL}/baixar/${fileId}`);
      if (!response.ok) throw new Error('Erro ao baixar o arquivo');
      
      const arquivo = await response.json();
      
      // Array binário
      const bin = atob(arquivo.content);
      const array = new Array(bin.length);
      for (let i = 0; i < bin.length; i++) {
        array[i] = bin.charCodeAt(i);
      }

      let mime = "application/octet-stream";
      const ext = arquivo.name.split('.').pop().toLowerCase();

      // Verifica o tipo de arquivo
      if (ext === 'pdf') mime = 'application/pdf';
      if (ext === 'doc') mime = 'application/msword';
      if (ext === 'docx') mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

      // Vira blob e cria link para download
      const blob = new Blob([new Uint8Array(array)], { type: mime });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');

      link.href = url;
      link.download = arquivo.name;
      link.click();
      // Deleta o link e revoga a URL para liberar memória
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
  }

  // 5. ADICIONAR NOVOS ARQUIVOS (BOTÃO FLUTUANTE DE MAIS)
  btnFloatingAdd.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    for (const file of files) {
      const ext = file.name.split('.').pop().toLowerCase();

      const parsedId = localStorage.getItem("id");
      const data = await convertorArquivos(file);
      
      const newFile = {
         type: (ext === 'doc' || ext === 'docx') ? 'doc' : 'pdf',
         name: file.name,
         content: data,
         pac_id: profile === 'PATIENT' ? parsedId : null,
         med_id: profile === 'DOCTOR' ? parsedId : null
       };
      try {
         const response = await fetch(`${API_URL}/salvar`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(newFile)
         });
        if (response.ok) {
           loadLibrary();
         } else {
           throw new Error('Erro no POST');
         }
       } catch (err) {
        console.warn('Erro ao enviar arquivo:', err);
       }
      };
      fileInput.value = '';
    })
    loadLibrary();
});