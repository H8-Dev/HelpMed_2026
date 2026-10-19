from sqlalchemy import text, update #type: ignore

from models.database import db
from models.arquivos_model import Arquivo

class ArquivoRepository:

    @staticmethod
    def buscar_arquivo_por_user(id):
        banco = db.session.get_bind().dialect.name

        if banco == "mysql":
            query = text("SELECT * FROM arquivos WHERE CAST(REGEXP_REPLACE(a_pac_id, '[^0-9]', '') AS SIGNED) = :id OR CAST(REGEXP_REPLACE(a_med_id, '[^0-9]', '') AS SIGNED) = :id")
            result = db.session.execute(query, {"id": id})
            arquivo_data = result.mappings().all()
            result.close()

            return [Arquivo(**dict(arquivo)) for arquivo in arquivo_data]
        return (Arquivo.query.filter((Arquivo.a_pac_id == id) | (Arquivo.a_med_id == id)).all())

    @staticmethod
    def buscar_arquivos_por_paciente_e_medico(pac_id, med_id):
        banco = db.session.get_bind().dialect.name

        if banco == "mysql":
            query = text("SELECT * FROM arquivos WHERE CAST(REGEXP_REPLACE(a_med_id, '[^0-9]', '') AS SIGNED) = :med_id and CAST(REGEXP_REPLACE(a_pac_id, '[^0-9]', '') AS SIGNED) = :pac_id")
            result = db.session.execute(query, {"med_id": med_id, "pac_id": pac_id})
            arquivo_data = result.mappings().all()
            result.close()

            return [Arquivo(**dict(arquivo)) for arquivo in arquivo_data]
        return (Arquivo.query.filter(Arquivo.pac_id == pac_id and Arquivo.med_id == med_id).all())

    #@staticmethod
    #def compartilhar_arquivo_com_medico(arq_id, med_id):
    #    banco = db.session.get_bind().dialect.name
#
    #    if banco == "mysql":
    #        query = text("UPDATE arquivos SET a_med_id = :med_id WHERE arq_id = :arq_id")
    #        result = db.session.execute(query, {"med_id": med_id, "arq_id": arq_id})
    #        result.close()
    #        return True
#
    #    arquivo = 
    #    
    #    return True