from sqlalchemy import text, case, label #type: ignore

from models.database import db
from models.pacientes_model import Paciente

class PacientesRepository:
    @staticmethod
    def login_paciente(cpf, senha):
        banco = db.session.get_bind().dialect.name
        
        if banco == "mysql":
            query = text("CALL sp_login_paciente(:cpf, :senha)")
            resultado = db.session.execute(query, {"cpf": cpf, "senha": senha})
            check = resultado.mappings().first()
            resultado.close()
            return check

        return {
            Paciente.senha,
            case(
                (Paciente.senha == senha, True),
                else_=False
            ).label("check").filter(Paciente.cpf == cpf)
        }
