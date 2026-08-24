const API_URL = "http://127.0.0.1:5000/arquivos";

const arquivo = document.getElementById("area_arquivo");

const response = await fetch(`${API_URL}/${encodeURIComponent(pac_id)}`);
const documentos = response;

function mudarDocumento(idDoc) {
  
  arquivo.value = documentos[id];
}

mudarDocumento('doc1');


function ferramentaDeBusca(palavaChave){
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
            resultados.push({
                elementoPai: node.parentNode,
                textoCompleto: node.nodeValue.trim()
            });
        }
    }
    return resultados;
}