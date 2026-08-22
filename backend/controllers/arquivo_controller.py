from flask import jsonify, request, Blueprint #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore

from models.database import db

from services.arquivo.buscar_arquivo_pacid_service import BuscarArquivoPorPaciente
from services.arquivo.salvar_arquivo_service import SalvarArquivoService

arq_controller = Blueprint("arq_controller", __name__)

class ArquivoController:

    @arq_controller.post('/arquivos/salvar')
    def salvar_arquivo():
        try:
            body = request.get_json(silent=True) or request.form
            dados = {
                "type": str(body['type']),
                "url": str(body['url']),
                "pac_id": str(body['pac_id']),
                "med_id": str(body['med_id'])
            }

            service = SalvarArquivoService()
            arquivo = service.salvar(dados)
            return jsonify(arquivo), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao salvar o arquivo"}), 500

    @arq_controller.get('/arquivos/<string:pac_id>')
    def buscar_arquivos_do_paciente(pac_id):

        service = BuscarArquivoPorPaciente()
        med_id = request.get_json(silent=True)
        arquivos = service.executar(pac_id, med_id)

        if not arquivos:
            return jsonify({"error": "Nenhum arquivo compartilhado com este paciente."}), 404

        return jsonify(arquivos), 200