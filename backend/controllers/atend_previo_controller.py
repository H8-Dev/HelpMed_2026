from flask import jsonify, request, Blueprint #type: ignore

from models.database import db

from services.chat.criar_atend_previo_service import CriarAtendPrevioService

prev_controller = Blueprint("prev_controller", __name__)

class AtendPrevioController:

    @prev_controller.post('/chat/previo')
    def create_previo():
        try:
            body = request.get_json(silent=True)
            if body is None:
                body = request.form.to_dict()

            paciente = str(body.get("paciente", ""))

            service = CriarAtendPrevioService()
            service.executar(paciente)
            return 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Erro ao criar atendimento prévio."}), 500