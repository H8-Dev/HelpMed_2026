from sqlalchemy import text #type: ignore

from models.database import db
from models.chat_model import Chat

class ChatRepository:

    @staticmethod
    def buscar_chats_user(id):
        query = text("CALL sp_buscar_chats(:id)")
        result = db.session.execute(query, {"id": id})
        chat_data = result.mappings().all()
        result.close()

        return [Chat(**dict(chat)) for chat in chat_data]

    @staticmethod
    def criar_atendimento_previo(id):
        query = text("CALL sp_atend_previo(:id)")
        result = db.session.execute(query, {"id": id})
        db.session.commit()
        chat_data = result.mappings().first()
        result.close()

        return [Chat(**dict(chat)) for chat in chat_data]