from flask import jsonify, request, Blueprint #type: ignore

from models.database import db

from services.chat.buscar_chat_cod_service import BuscarChatCodService


atend_controller = Blueprint("atend_controller", __name__)

class AtendimentoController:
    @atend_controller.get('/chats/check')
    def check():
        return jsonify({"status": "ok"}), 200

    @atend_controller.get('/chats/<int:id>')
    def get_chat_list(id):
        try:
            service = BuscarChatCodService()
            chats = service.executar(id)

            return jsonify(chats), 200
        except ValueError:
            return jsonify({"error": "Erro."}), 500

## @atend_controller.post('/chats')
## def gerarAtend(paciente, medico, av):
