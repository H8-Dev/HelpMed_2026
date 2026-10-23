from models.medico_model import Medico
from repositories.medicos_repository import MedicosRepository

class UpdateMedicoService:
    def executar(self, crm, dados):
        medico = Medico.buscar_crm(crm)
        if not medico:
            raise ValueError("Médico não existe.")

        email_existente = MedicosRepository.buscar_email(dados["email"])
        if email_existente:
            if email_existente.crm != medico.crm:
                raise ValueError("Email já cadastrado.")

        senha = dados.get("senha")
        if senha is "":
            senha = None
        formacao = dados.get("formacao")
        if formacao is "":
            formacao = None

        medico.atualizar(
            senha=senha,
            email=dados.get("email"),
            formacao=formacao,
        )

        return medico.to_dict()