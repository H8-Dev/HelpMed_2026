from models.medico_model import Medico
from repositories.medicos_repository import MedicosRepository

class UpdateMedicoService:
    def executar(self, medico_crm, dados):
        medico = Medico.buscar_crm(medico_crm)
        if not medico:
            return None

        required = ["senha", "nome", "sobrenome", "email"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")

        email_existente = MedicosRepository.buscar_email(dados["email"])
        if email_existente:
            raise ValueError("Email já cadastrado.") 

        medico.atualizar(
            senha=dados.get("senha"),
            nome=dados.get("nome"),
            sobrenome=dados.get("sobrenome"),
            email=dados.get("email"),
            formacao=dados.get("formacao"),
        )

        return medico.to_dict()