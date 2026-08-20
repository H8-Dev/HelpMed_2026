from models.pacientes_model import Paciente

class BuscarPacCpfService:
    def executar(self, paciente_cpf):
        paciente = Paciente.buscar_cpf(paciente_cpf)
    
        if paciente is None:
            return None
    
        return paciente.to_dict()