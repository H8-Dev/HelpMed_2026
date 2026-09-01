const API_URL = "http://127.0.0.1:5000/arquivos";

const arquivo = document.getElementById("area_arquivo");


async function fetchDocumentos() {
    try {
        const response = await fetch(`${API_URL}/${encodeURIComponent(pac_id)}`);
        const documentos = await response.json();
        return documentos;
    } catch (error) {
        console.error("Erro ao buscar documentos:", error);
    }
}

function mudarDocumento(idDoc) {
  
  arquivo.value = documentos[id];
}


function ferramentaDeBusca(){
    const palavaChave = document.getElementById('searchInput').value.trim();
    const resultados_pesquisa = [];
    const regex = new RegExp(palavaChave, 'i');
    let node;

    const busca = document.createTreeWalker(
        arquivo,
        NodeFilter.SHOW_TEXT,
        null, false
    );

    while (node = busca.nextNode()){
        if (regex.test(node.nodeValue)){
            resultados_pesquisa.push({
                elementoPai: node.parentNode,
                textoCompleto: node.nodeValue.trim()
            });
        }
    }
    return resultados_pesquisa;
}

function toggleModal(show) {
      const modal = document.getElementById('modalBusca');
      if (show == "True") {
        modal.classList.add('active');
      } else {
        modal.classList.remove('active');
      }
    }