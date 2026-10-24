from repositories.chat_repository import ChatRepository

class CriarAtendPrevioService:
    def executar(self, id):
        if not id:
            raise ValueError("Id do usuário não recebido.")

        chat = ChatRepository.criar_atendimento_previo(id)
        if chat:
            return True
        else: return False