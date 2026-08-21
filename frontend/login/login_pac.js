const API_URL = "http://127.0.0.1:5000/pacientes/buscar";


const form = document.querySelector(".login-form");
const pacId = document.querySelector("#cpf")
const campoSenha = document.querySelector("#senha");

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