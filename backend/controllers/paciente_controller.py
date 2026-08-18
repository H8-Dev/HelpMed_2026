from flask import jsonify, request, Blueprint #type: ignore

from models.database import db

from services.paciente.cadastrar_paciente_service import CriarPacienteService

pac_controller = Blueprint("pac_controller", __name__)

@pac_controller.post('/cadastrar')
def cadastrar_paciente():
    try:
        dados = {
            "cpf": str(request.form['cpf']),
            "senha": str(request.form['senha']),
            "nome": str(request.form['nome']),
            "sobrenome": str(request.form['sobrenome']),
            "email": str(request.form['email'])
        }

        service = CriarPacienteService()
        paciente = service.cadastrar(dados)
        return jsonify(paciente), 201
    
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except SQLAlchemyError: #type: ignore
        db.session.rollback()
        return jsonify({"error": "Erro ao cadastrar paciente."}), 500