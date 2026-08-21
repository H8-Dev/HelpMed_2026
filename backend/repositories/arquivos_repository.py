from sqlalchemy import text #type: ignore

from models.database import db
from models.arquivos_model import Arquivo

class ArquivoRepository:
    @staticmethod
    def buscar_arquivos_por_medico(med_id):
        query = text("SELECT * FROM arquivos WHERE med_id = :med_id")
        result = db.session.execute(query, {"med_id": med_id})
        arquivo_data = result.mappings().all()
        result.close()

        return [Arquivo(**dict(arquivo)) for arquivo in arquivo_data]

    @staticmethod
    def buscar_arquivos_por_paciente(pac_id):
        query = text("SELECT * FROM arquivos WHERE pac_id = :pac_id")
        result = db.session.execute(query, {"pac_id": pac_id})
        arquivo_data = result.mappings().all()
        result.close()

        return [Arquivo(**dict(arquivo)) for arquivo in arquivo_data]

    @staticmethod
    def buscar_arquivos_por_paciente_e_medico(pac_id, med_id):
        query = text("SELECT * FROM arquivos WHERE med_id = :med_id and pac_id = :pac_id")
        result = db.session.execute(query, {"med_id": med_id}, {"pac_id": pac_id})
        arquivo_data = result.mappings().all()
        result.close()

        return [Arquivo(**dict(arquivo)) for arquivo in arquivo_data]