const API_URL = "http://127.0.0.1:5000/medicos/cadastrar";

const form = document.getElementById("form-medico");
const medId = document.querySelector("#crm")
const campoCPF = document.querySelector("#cpf");
const campoSenha = document.querySelector("#senha");
const campoNome = document.querySelector("#nome");
const campoSobrenome = document.querySelector("#sobrenome");
const campoEmail = document.querySelector("#email");
const campoFormacao = document.querySelector("#formacao");


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

function formatarCPF() {
    var campoCPF = document.getElementById("cpf").value;
    if(campoCPF[3]!="."){
        if(campoCPF[3]!= undefined){
            document.getElementById("cpf").value=campoCPF.slice(0,3)+"."+campoCPF[3]
        }}

    if(campoCPF[7]!="."){
        if(campoCPF[7]!= undefined){
            document.getElementById("cpf").value=campoCPF.slice(0,7)+"."+campoCPF[7]
        }}

    if(campoCPF[11]!="-"){
        if(campoCPF[11]!= undefined){
            document.getElementById("cpf").value=campoCPF.slice(0,11)+"-"+campoCPF[11]
        }}
}


async function cadastrarMedico() {
    
    const dados = {
        "crm": medId.value,
        "cpf": campoCPF.value,
        "senha": campoSenha.value,
        "nome": campoNome.value,
        "sobrenome": campoSobrenome.value,
        "email": campoEmail.value,
        "formacao": campoFormacao.value
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });
        console.log("Resposta do cadastro: " + response);
        header("home/home.html");
    }
    catch (error) {
        console.error("Erro de conexão com a API:", "error");
    }
}