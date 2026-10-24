from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.chat.criar_atend_previo_service import CriarAtendPrevioService
from services.chat.message_atend_virtual_service import MessageAtendVirtualService

prev_controller = Blueprint("prev_controller", __name__)

class AtendPrevioController:

    @prev_controller.post('/chats/previo')
    def create_previo():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.json or {}

            id = str(body.get("id"))

            service = CriarAtendPrevioService()
            chat = service.executar(id)
            if chat:
                return jsonify({"message": "Sucesso."}), 201

        except ValueError as error:
            print(error)
            return jsonify({"error": str(error)}), 400

    @prev_controller.post('/chats/messages') #NotDone
    def nova_msg_ia():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.form.to_dict()

            chat = str(body.get("chat_id", ""))
            mensagem = str(body.get("mensagem", ""))

            service = MessageAtendVirtualService()
            service.executar(chat, mensagem)

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Erro ao enviar mensagem."}), 500