from flask import jsonify, request, Blueprint, send_file #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore
import io

from models.database import db

from services.arquivo.buscar_arquivo_paciente_service import BuscarArquivoPorPaciente
from services.arquivo.salvar_arquivo_service import SalvarArquivoService
from services.arquivo.buscar_arquivo_por_id_service import BuscarArquivoPorId

arq_controller = Blueprint("arq_controller", __name__)

class ArquivoController:

    @arq_controller.post('/arquivos/salvar')
    def salvar_arquivo():
        try:
            body = request.get_json(silent=True) or request.form
            dados = {
                "type": str(body['type']),
                "nome_arq": str(body['nome_arq']),
                "dados": str(body['dados']),
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

    @arq_controller.post('/arquivos')
    def buscar_arquivos_do_paciente():

        body = request.get_json(silent=True) or request.form
        pac_id = str(body['pac_id'])
        med_id = str(body['med_id'])

        service = BuscarArquivoPorPaciente()
        arquivos = service.executar(pac_id, med_id)

        if not arquivos:
            return jsonify({"error": "Nenhum arquivo compartilhado com este paciente."}), 404

        return jsonify(arquivos), 200

    @arq_controller.get('/arquivos/<int:arq_id>')
    def buscar_arquivo_por_id(arq_id):
        service = BuscarArquivoPorId()
        arquivo = service.executar(arq_id)

        if not arquivo:
            return jsonify({"error": "Arquivo não encontrado."}), 404

        return send_file(
            io.BytesIO(arquivo.dados),
            mimetype='text/plain'
        ), 200

    @arq_controller.put('/arquivos/<int:arq_id>')
    def atualizar_arquivo(arq_id):
        return;