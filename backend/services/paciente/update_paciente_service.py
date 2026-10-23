from models.pacientes_model import Paciente
from repositories.pacientes_repository import PacientesRepository

class UpdatePacienteService:
    def executar(self, cpf, dados):
        paciente = Paciente.buscar_cpf(cpf)
        if not paciente:
            return None

        email_existente = Paciente.buscar_email(dados["email"])
        if email_existente:
            if email_existente.cpf != paciente.cpf:
                raise ValueError("Email já cadastrado.") 

        senha = dados.get("senha")
        if senha is "":
            senha = None

        print(senha)
        paciente.atualizar(
            senha=senha,
            email=dados.get("email"),
        )

        return paciente.to_dict()