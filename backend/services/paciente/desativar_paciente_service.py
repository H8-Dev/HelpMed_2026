from repositories.pacientes_repository import PacientesRepository
from models.pacientes_model import Paciente

class DesativarPacienteService:
    def desativar(self, cpf):

        cpf = f"{str(cpf)[:3]}.{str(cpf)[3:6]}.{str(cpf)[6:9]}-{str(cpf)[9:]}"
        paciente = Paciente.buscar_cpf(cpf)
        if not paciente:
            return False

        paciente.atualizar(ativo=False)
        return True

        
