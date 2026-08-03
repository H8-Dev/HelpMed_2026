from datetime import datetime
from models.pacientes_model import Paciente

class CriarPacienteService:
    def cadastrar(self, dados):
        required = ["cpf", "senha", "nome", "sobrenome", "email"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")
            
        cpf_existente = Paciente.buscar_cpf(dados["cpf"])
        if cpf_existente:
            raise ValueError("Este CPF já está cadastrado.")
        
        paciente = Paciente(
            cpf = dados["cpf"],
            senha =  dados["senha"],
            nome =  dados["nome"],
            sobrenome =  dados["sobrenome"],
            email =  dados["email"],
            data_create = datetime.now().timestamp()
        )

        paciente.salvar()
        return