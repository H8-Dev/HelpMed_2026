from repositories.chat_repository import ChatRepository

class EnviarMensagemChat:
    def executar(self, chat_id, mensagem):

        if not chat_id or not mensagem:
            print("Error 400\n", chat_id, "\n", mensagem)
            raise ValueError("Elementos da função estão faltando.")

        status = ChatRepository.enviar_mensagem(chat_id, mensagem)

        if status: return True
        else:
            raise Exception("Erro durante a execução.")