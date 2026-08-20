from flask import jsonify, request, Blueprint #type: ignore

from models.database import db

from services.paciente.buscar_cpf_service import BuscarPacCpfService
from services.paciente.cadastrar_paciente_service import CriarPacienteService

pac_controller = Blueprint("pac_controller", __name__)


class PacienteController:

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

    @pac_controller.get('/buscar/<string:paciente_cpf>')
    def buscar_paciente_por_cpf(paciente_cpf):

        service = BuscarPacCpfService()
        paciente = service.executar(paciente_cpf)

        if paciente is None:
            return jsonify({"error": "Paciente não encontrado."}), 404

        return jsonify(paciente), 200