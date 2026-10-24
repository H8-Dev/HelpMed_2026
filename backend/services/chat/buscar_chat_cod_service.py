from repositories.chat_repository import ChatRepository

class BuscarChatCodService:
    def executar(self, id):
        chats = ChatRepository.buscar_chats_user(id)

        if not chats:
            raise ValueError("Falha")

        return [chat.to_dict() for chat in chats]