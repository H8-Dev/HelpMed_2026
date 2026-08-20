from sqlalchemy import text #type: ignore

from models.database import db
from models.medico_model import Medico

class MedicosRepository:
    @staticmethod
    def buscar_formacao(formacao):
        query = text("SELECT * FROM medicos WHERE formacao = :formacao")
        result = db.session.execute(query, {"formacao": formacao})
        medicos = result.mappings().all()
        result.close()

        return [Medico(**dict(medico)) for medico in medicos]
