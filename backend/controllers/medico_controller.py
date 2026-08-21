from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.medico.cadastrar_medico_service import CriarMedicoService
from services.medico.buscar_crm_service import BuscarMedicoPorCRMService
from services.medico.buscar_formacao_service import BuscarMedicoPorFormacaoService

med_controller = Blueprint("med_controller", __name__)

class MedicoController:
    
    @med_controller.post('/medicos/cadastrar')
    def cadastrar_medico():
        try:
            body = request.get_json(silent=True) or request.form
            dados = {
                "crm": str(body['crm']),
                "cpf": str(body['cpf']),
                "senha": str(body['senha']),
                "nome": str(body['nome']),
                "sobrenome": str(body['sobrenome']),
                "email": str(body['email']),
                "formacao": str(body['formacao'])
            }

            service = CriarMedicoService()
            medico = service.cadastrar(dados)
            return jsonify(medico), 201

    
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao cadastrar médico."}), 500


    @med_controller.get('/medicos/buscar/<string:medico_crm>')
    def buscar_medico_por_crm(medico_crm):

        service = BuscarMedicoPorCRMService()
        medico = service.executar(medico_crm)

        if medico is None:
            return jsonify({"error": "Médico não encontrado."}), 404

        return jsonify(medico), 200

    @med_controller.get('/medicos/buscar/formacao/<string:formacao>')
    def buscar_medico_por_formacao(formacao):

        service = BuscarMedicoPorFormacaoService()
        medicos = service.executar(formacao)

        if not medicos:
            return jsonify({"error": "Nenhum médico encontrado com essa formação."}), 404

        return jsonify(medicos), 200