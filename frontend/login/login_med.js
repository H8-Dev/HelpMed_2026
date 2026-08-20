const API_URL = "http://127.0.0.1:5000/buscar";

const form = document.querySelector("#form-medico");
const medId = document.querySelector("#crm")
const campoCPF = document.querySelector("#cpf");
const campoSenha = document.querySelector("#senha");


function formatarCRM() {
    var campoCRM = document.getElementById("crm").value;
    if(campoCRM[6]!="/"){
        if(campoCRM[6]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,6)+"/"+campoCRM[6]
        }}
    if(campoCRM[7]!="B"){
        if(campoCRM[7]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,7)+"B"+campoCRM[7]
        }}
    if(campoCRM[8]!="R"){
        if(campoCRM[8]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,8)+"R"+campoCRM[8]
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