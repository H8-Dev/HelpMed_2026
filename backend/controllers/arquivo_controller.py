from flask import jsonify, request, Blueprint, send_file #type: ignore
from sqlalchemy.exc import SQLAlchemyError #type: ignore
import io, base64, os, re
from docx import Document #type: ignore 
from pypdf import PdfReader #type: ignore

from models.database import db

from services.arquivo.buscar_arquivo_user_service import BuscarArquivoPorUser
from services.arquivo.buscar_arquivo_paciente_service import BuscarArquivoPorPaciente
from services.arquivo.salvar_arquivo_service import SalvarArquivoService
from services.arquivo.buscar_arquivo_por_id_service import BuscarArquivoPorId

arq_controller = Blueprint("arq_controller", __name__)

class ArquivoController:

    def texto_limpo(nome, dados):
        tipo = os.path.splitext(nome)
        tipo = tipo[1]
        texto_limpo = ""

        if (
            dados.startswith(b"JVBER")
            or dados.startswith(b"UEsDB")
            or dados.startswith(b"0M8R4")
        ):
            arq = io.BytesIO(base64.b64decode(dados.decode('utf-8')))
        else:
            arq = io.BytesIO(dados)

        if tipo == ".docx" or tipo == ".doc":
            doc = Document(arq)
            texto_limpo = [p.text for p in doc.paragraphs]
            texto_limpo = "\n".join(texto_limpo).strip()

        elif tipo == ".pdf":
                
            pdf = PdfReader(arq)
            texto_limpo = []

            for page in pdf.pages:
            
                txt_pag = (page.extract_text(extraction_mode="layout") or "")
                txt_pag_l = [linha.rstrip() for i, linha in enumerate(txt_pag.split('\n')) if linha.strip()]
                texto_limpo.append("\n".join(txt_pag_l))
            
            texto_limpo = "\n".join(texto_limpo)

        return texto_limpo.strip()

    @arq_controller.get('/arquivos/usuario/<int:id>')
    def buscar_arquivos_do_paciente(id):
        service = BuscarArquivoPorUser()
        arquivos = service.executar(id)

        if not arquivos:
            return jsonify({"error": "Nenhum arquivo encontrado para este paciente."}), 204

        return jsonify([{
            "id": arquivo['arq_id'],
            "type": arquivo['type'],
            "content": ArquivoController.texto_limpo(arquivo['nome_arq'], arquivo['dados']),
            "name": arquivo['nome_arq'],
            "pac_id": arquivo['a_pac_id'],
            "med_id": arquivo['a_med_id'],
            "last_update": arquivo['last_update']
        } for arquivo in arquivos]), 200

    @arq_controller.post('/arquivos/salvar')
    def salvar_arquivo():
        try:
            body = request.get_json(silent=True) or request.form
            blob = body['content']

            dados = {
                "type": str(body['type']),
                "nome_arq": str(body['name']),
                "dados": base64.b64decode(blob.encode('utf-8')),
                "a_pac_id": str(body['pac_id']) if body.get('pac_id') else None,
                "a_med_id": str(body['med_id']) if body.get('med_id') else None
            }

            service = SalvarArquivoService()
            arquivo = service.salvar(dados)
            return jsonify("Novo arquivo salvo com sucesso."), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Erro ao salvar o arquivo"}), 500

    @arq_controller.post('/arquivos_med')
    def buscar_arquivos_do_paciente_com_medico():

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
        
        return jsonify({"content": ArquivoController.texto_limpo(arquivo['nome_arq'], arquivo['dados'])}), 200


    @arq_controller.get('/arquivos/baixar/<int:arq_id>')
    def baixar_arquivo(arq_id):
        service = BuscarArquivoPorId()
        arquivo = service.executar(arq_id)

        if not arquivo:
            return jsonify({"error": "Arquivo não encontrado."}), 404

        return jsonify({"name": arquivo['nome_arq'],
                        "content": base64.b64encode(arquivo['dados']).decode('utf-8')}), 200

    @arq_controller.put('/arquivos/<int:arq_id>')
    def atualizar_arquivo(arq_id):
        return