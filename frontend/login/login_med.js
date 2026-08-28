const API_URL = "http://127.0.0.1:5000/medicos/login";

const form = document.querySelector("#form-medico");
const medId = document.querySelector("#crm")
const campoSenha = document.querySelector("#senha");

if (form){
    form.addEventListener('submit', function(event){
        event.preventDefault();
    });
} else {
    console.log("Falhou.")
}


function formatarCRM() {
    var campoCRM = document.getElementById("crm").value;
    if(campoCRM[6]!="-"){
        if(campoCRM[6]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,6)+"-"
        }}
    if(campoCRM[7]!="B"){
        if(campoCRM[7]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,7)+"B"
        }}
    if(campoCRM[8]!="R"){
        if(campoCRM[8]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,8)+"R"
        }}
}

async function loginMedico(){

    const dados = {
        "crm": medId.value,
        "senha": campoSenha.value
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });
        console.log("Resposta do pedido de login: " + response);
        header("home/home.html");
    } catch (error) {
        console.error("Erro de conexão com a API:", "error");
    }
}