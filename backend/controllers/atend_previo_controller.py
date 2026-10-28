from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.chat.criar_atend_previo_service import CriarAtendPrevioService

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