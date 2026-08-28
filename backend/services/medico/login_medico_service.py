from repositories.medicos_repository import MedicosRepository

class LoginMedicoService:
    def login(self, crm, senha):
        
        check = MedicosRepository.login_medico(crm, senha)
        return check
                    
                