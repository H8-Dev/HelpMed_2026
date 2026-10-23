from repositories.pacientes_repository import PacientesRepository
from models.pacientes_model import Paciente

class EmailPacienteService:
    def executar(self, cpf):



        cpf_existente = Paciente.buscar_cpf(cpf)
        if not cpf_existente:
            raise ValueError("Paciente não existe.")

        email = Paciente.buscar_email(cpf_existente.email)

        return email