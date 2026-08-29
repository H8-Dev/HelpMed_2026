const API_URL = "http://127.0.0.1:5000/pacientes/cadastrar";

const form = document.querySelector(".login-form");
const pacId = document.querySelector("#cpf")
const campoSenha = document.querySelector("#senha");
const campoNome = document.querySelector("#nome");
const campoSobrenome = document.querySelector("#sobrenome");
const campoEmail = document.querySelector("#email");

if (form){
    form.addEventListener('submit', function(event){
        event.preventDefault();
    });
} else {
    console.log("Falhou.")
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

async function cadastrarPaciente() {

    const dados = {
        cpf: pacId.value,
        senha: campoSenha.value,
        nome: campoNome.value,
        sobrenome: campoSobrenome.value,
        email: campoEmail.value
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
        window.location.href = "home/home.html";
    } catch (error) {
        console.error("Erro de conexão com a API:", "error");
    }
}