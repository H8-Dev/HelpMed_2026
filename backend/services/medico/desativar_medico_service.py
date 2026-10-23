from repositories.medicos_repository import MedicosRepository
from models.medico_model import Medico

class DesativarMedicoService:
    def desativar(self, crm):

        crm = f"{crm:06d}-BR"
        medico = Medico.buscar_crm(crm)
        if not medico:
            raise ValueError("Médico não existe.")

        medico.atualizar(ativo=False)
        return True

        
