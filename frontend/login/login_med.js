const form = document.querySelector("#form-medico");
const medId = document.querySelector("#crm")
const campoCPF = document.querySelector("#cpf");
const campoSenha = document.querySelector("#senha");
const campoNome = document.querySelector("#nome");
const campoSobrenome = document.querySelector("#sobrenome");
const campoEmail = document.querySelector("#email");
const campoFormacao = document.querySelector("#formacao");


function formatarCRM() {
    var campoCRM = document.getElementById("crm").value;
    if(campoCRM[6]!="/"){
        if(campoCRM[6]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,6)+"/"+campoCRM[6]
        }}
    if(campoCRM[7]!="B"){
        if(campoCRM[7]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,11)+"B"+campoCRM[7]
        }}
    if(campoCRM[8]!="R"){
        if(campoCRM[8]!= undefined){
            document.getElementById("crm").value=campoCRM.slice(0,12)+"R"+campoCRM[8]
        }}
}