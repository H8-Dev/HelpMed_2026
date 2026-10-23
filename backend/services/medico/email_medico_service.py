from repositories.medicos_repository import MedicosRepository

class EmailMedicoService:
    def executar(crm):

        crm_existente = MedicosRepository.buscar_crm(crm)
        if not crm_existente:
            raise ValueError("Médico não existe.")

        email = MedicosRepository.buscar_email(crm_existente["email"])

        return {"email": email}