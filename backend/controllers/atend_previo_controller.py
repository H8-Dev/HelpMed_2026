import json

from flask import jsonify, request, Blueprint #type: ignore

from models.database import db

from services.chat.criar_atend_previo_service import CriarAtendPrevioService
from services.chat.enviar_mensagem_previo_service import EnviarMensagemChatPrevio

prev_controller = Blueprint("prev_controller", __name__)

class AtendPrevioController:

    @prev_controller.post('/chats/previo')
    def create_previo():
        try:
            body = request.get_json(silent=True) or request.json

            id = str(body['id'])

            service = CriarAtendPrevioService()
            chat = service.executar(id)
            if chat:
                return jsonify({"message": "Sucesso."}), 201

        except ValueError as error:
            print(error)
            return jsonify({"error": str(error)}), 400

    @prev_controller.post('/chats/messages-ia')
    def nova_msg():
        try:
            body = request.get_json(silent=True) or request.form.to_dict()

            chat = str(body['id'])
            mensagem = body['message']

            mensagem_limpa = json.dumps(mensagem)
            

            service = EnviarMensagemChatPrevio()
            service.executar(chat, mensagem_limpa)

            return jsonify("Mensagem enviada com sucesso."), 200

        except ValueError as error:
            print("Erro ao enviar mensagem:", str(error))
            return jsonify({"error": str(error)}), 400

        except Exception as e:
            db.session.rollback()
            print("Erro ao enviar mensagem:", str(e))
            return jsonify({"error": "Erro ao enviar mensagem."}), 500
