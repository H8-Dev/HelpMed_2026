from sqlalchemy import text #type: ignore

from models.database import db
from models.chat_model import Chat

class ChatRepository:
    @staticmethod
    def buscar_chat_por_medico(med_id):
        query = text("SELECT * FROM chats WHERE med_id = :med_id")
        result = db.session.execute(query, {"med_id": med_id})
        chat_data = result.mappings().all()
        result.close()

        return [Chat(**dict(chat)) for chat in chat_data]

    @staticmethod
    def buscar_chat_por_paciente(pac_id):
        query = text("SELECT * FROM chats WHERE pac_id = :pac_id")
        result = db.session.execute(query, {"pac_id": pac_id})
        chat_data = result.mappings().all()
        result.close()

        return [Chat(**dict(chat)) for chat in chat_data]