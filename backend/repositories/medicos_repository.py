from sqlalchemy import text, case, label #type: ignore

from models.database import db
from models.medico_model import Medico

class MedicosRepository:
    @staticmethod
    def buscar_formacao(formacao):
        banco = db.session.get_bind().dialect.name

        if banco == "mysql":
            query = text("SELECT * FROM medicos WHERE formacao = :formacao")
            result = db.session.execute(query, {"formacao": formacao})
            medicos = result.mappings().all()
            result.close()
            return [Medico(**dict(medico)).lower for medico in medicos]
        
        return (Medico.query.filter(Medico.formacao == formacao).all())

    @staticmethod
    def buscar_email(email):
        banco = db.session.get_bind().dialect.name

        if banco == "mysql":
            query = text("SELECT * FROM medicos WHERE email = :email")
            result = db.session.execute(query, {"email": email})
            medicos = result.mappings().all()
            result.close()
            return [Medico(**dict(medico.lower)) for medico in medicos]
        
        return (Medico.query.filter(Medico.email == email).all())

    @staticmethod
    def login_medico(crm, senha):
        banco = db.session.get_bind().dialect.name
        
        if banco == "mysql":
            query = text("CALL sp_login_medico(:crm, :senha)")
            resultado = db.session.execute(query, {"crm": crm, "senha": senha})
            check = resultado.mappings().first()
            resultado.close()
            return check

        return {
            Medico.senha,
            case(
                (Medico.senha == senha, True),
                else_=False
            ).label("check").filter(Medico.crm == crm)
        }
