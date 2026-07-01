from datetime import datetime
from models.medico_model import Medico

class CriarMedicoService:
    def cadastrar(self, dados):
        required = ["crm", "cpf", "senha", "nome", "sobrenome", "email"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")
            
        crm_existente = Medico.buscar_crm(dados["crm"])
        if crm_existente:
            raise ValueError("Já existe um médico com o CRM fornecido!!")
        
        medico = Medico(
            crm = dados["crm"],
            cpf = dados["cpf"],
            senha =  dados["senha"],
            nome =  dados["nome"],
            sobrenome =  dados["sobrenome"],
            email =  dados["email"],
            data_create = datetime.now().timestamp()
        )

        medico.salvar()
        return