const form = document.querySelector(".login-form");
const medId = document.querySelector("#crm")
const campoCPF = document.querySelector("#cpf");
const campoSenha = document.querySelector("#senha");
const campoNome = document.querySelector("#nome");
const campoSobrenome = document.querySelector("#sobrenome");
const campoEmail = document.querySelector("#email");
const campoFormacao = document.querySelector("#formacao");


function formatarCRM() {
    var campoCRM = document.querySelector("#crm");
    if(campoCRM[6]!="/"){
        if(campoCRM[10]!= undefined){
            document.querySelector("#crm").value=campoCRM.slice(0,10)+"/"+campoCRM[10]
        }}
    if(campoCRM[7]!="B"){
        if(campoCRM[11]!= undefined){
            document.querySelector("#crm").value=campoCRM.slice(0,11)+"B"+campoCRM[11]
        }}
    if(campoCRM[8]!="R"){
        if(campoCRM[12]!= undefined){
            document.querySelector("#crm").value=campoCRM.slice(0,12)+"R"+campoCRM[12]
        }}
}