from repositories.pacientes_repository import PacientesRepository

class LoginPacienteService:
    def login(self, cpf, senha):
        
        check = PacientesRepository.login_paciente(cpf, senha)
        return check
                    
                