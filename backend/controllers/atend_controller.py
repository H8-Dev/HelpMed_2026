from flask import jsonify, request, Blueprint #type: ignore
import json

from models.database import db

from services.chat.buscar_chat_cod_service import BuscarChatCodService
from services.chat.enviar_mensagem_service import EnviarMensagemChat


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
        except ValueError as error:
            return jsonify({"error": str(error)}), 500

    @atend_controller.post('/chats/messages') #MaybeDone
    def nova_msg():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.form.to_dict()

            chat = str(body.get("id"))
            mensagem = body.get("message")

            mensagem_limpa = json.dumps(mensagem)
            

            service = EnviarMensagemChat()
            service.executar(chat, mensagem_limpa)

            return jsonify("Mensagem enviada com sucesso!"), 204

        except ValueError as error:
            print("Erro ao enviar mensagem:", str(error))
            return jsonify({"error": str(error)}), 400

        except Exception as e:
            db.session.rollback()
            print("Erro ao enviar mensagem:", str(e))
            return jsonify({"error": "Erro ao enviar mensagem."}), 500

## @atend_controller.post('/chats')
## def gerarAtend(paciente, medico, av):
