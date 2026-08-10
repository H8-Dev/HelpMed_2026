from sqlalchemy import text #type: ignore

from models.database import db
from models.pagamentos_model import Pagamento

class PagamentoRepository:
    @staticmethod
    def buscar_pagamentos_por_medico(med_id):
        query = text("SELECT * FROM pagamentos WHERE med_id = :med_id")
        result = db.session.execute(query, {"med_id": med_id})
        pagamento_data = result.mappings().all()
        result.close()

        return [Pagamento(**dict(pagamento)) for pagamento in pagamento_data]

    @staticmethod
    def buscar_pagamentos_por_paciente(pac_id):
        query = text("SELECT * FROM pagamentos WHERE pac_id = :pac_id")
        result = db.session.execute(query, {"pac_id": pac_id})
        pagamento_data = result.mappings().all()
        result.close()

        return [Pagamento(**dict(pagamento)) for pagamento in pagamento_data]