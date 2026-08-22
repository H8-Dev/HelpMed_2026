const API_URL = "http://127.0.0.1:5000/medicos/buscar";

const form = document.querySelector("#form-medico");
const medId = document.querySelector("#crm")
const campoCPF = document.querySelector("#cpf");
const campoSenha = document.querySelector("#senha");


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


//VV Testes VV{
async function buscarMedico(){

    try{
        const response = await fetch(`${API_URL}/${medId.value}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const dados = await response.json();

        if (!response.ok) {
            showMessage(dados.error || "Médico não está cadastrado.", "error");
            return;
        }

    }catch (error) {
        console.error("Erro de conexão com a API:", "error");
    }

}
//} ^^ Testes ^^