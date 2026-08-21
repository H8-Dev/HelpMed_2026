const API_URL = "http://127.0.0.1:5000/arquivos/";

const arquivo = document.getElementById("area_arquivo");

// const documentos = {
//   doc1: "Este é o conteúdo do primeiro documento.",
//   doc2: "Aqui está o texto do segundo documento.",
//   doc3: "Por fim, este é o terceiro documento."
// };
// 
// function mudarDocumento(idDoc) {
//   const editor = document.getElementById("meuEditor");
//   editor.value = documentos[idDoc];
// }
// 
// mudarDocumento('doc1');


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