from repositories.chat_repository import ChatRepository

class CriarAtendPrevioService:
    def executar(self, paciente):
        if not paciente:
            raise ValueError("O campo 'paciente' é obrigatório.")

        chat = ChatRepository.criar_atendimento_previo(paciente)
        return chat