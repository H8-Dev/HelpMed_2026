from repositories.chat_repository import ChatRepository

class EnviarMensagemChat:
    def executar(self, chat_id, mensagem):

        if not chat_id or mensagem:
            raise ValueError("Elementos da função estão faltando.")

        status = ChatRepository.enviar_mensagem(chat_id, mensagem)

        if status is True: return True
        else: raise ValueError("Erro durante a execução.")