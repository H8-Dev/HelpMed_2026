const API_URL = "http://127.0.0.1:5000/arquivos";

const arquivo = document.getElementById("text-editor");
const abaLateral = document.getElementById("right-panel");
const nomeArq = document.getElementById("file-name");
const salvar = document.getElementById("saveBtn");

let arqAtivo = null;

async function fetchDocumentos() {
    pac_id = localStorage.getItem('pac_id');
    med_id = localStorage.getItem('med_id');
    const dados = {
        pac_id: pac_id,
        med_id: med_id
    };
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const documentos = await response.json();

        documentos.forEach(doc => {
            const novoDoc = document.createElement("div");
            novoDoc.className = "panel-box";
            novoDoc.textContent = `📄 ${doc.nome_arq}`;

            novoDoc.addEventListener("click", () => {
               document.querySelectorAll('.panel-box').forEach(box => box.classList.remove('active'));
                novoDoc.classList.add('active');

                mudarDocumento(doc.arq_id, doc.nome_arq);
            });
        })
    } catch (error) {
        console.error("Erro ao buscar documentos:", error);
    }
}

async function mudarDocumento(id, nome) {
    try {
        nomeArq.value = nome;

        const response = await fetch(`${API_URL}/${id}`);7

        const textoArq = await response.text();
        arqAtivo = id;
        arquivo.value = textoArq;
        
    } catch (error) {
        console.error("Erro ao buscar documento:", error);
        arquivo.value = `Erro ao carregar o documento: ${error.message}`;
    }
}

salvar.addEventListener("click", async () => {
    if (!arqAtivo) return;

    const dados = {
        arq_id: arqAtivo,
        nome_arq: nomeArq.value,
        dados: arquivo.value
    };

    try {
        const response = await fetch(`${API_URL}/${arqAtivo}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();
        if (response.ok) {
            alert("Documento salvo com sucesso!");
        } else{
            alert(`Erro ao salvar documento: ${result.error}`);
        }


    } catch (error) {
        console.error("Erro ao salvar documento:", error);
    }

});


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


window.addEventListener('DOMContentLoaded', function() {
    fetchDocumentos();
});