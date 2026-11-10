from models.arquivos_model import Arquivo
from models.chat_model import Chat

class CompartilharArquivoService:
    def executar(self, arq_id, chat_id):
        arquivo = Arquivo.buscar_arquivo(arq_id)
        if not arquivo:
            raise ValueError("Arquivo não encontrado.")

        chat = Chat.buscar_chat(chat_id)
        if not chat:
            raise ValueError("Chat não encontrado.")

        arquivo.atualizar(
            med_id=chat['med_id']
        )
        
        return arquivo.to_dict()