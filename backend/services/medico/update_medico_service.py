from datetime import datetime
from models.medico_model import Medico

class UpdateMedicoService:
    def atualizar(self, medico_crm, dados):
        medico = Medico.buscar_crm(medico_crm)
        if not medico:
            return None

        required = ["crm", "cpf", "senha", "nome", "sobrenome", "email"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")
            
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