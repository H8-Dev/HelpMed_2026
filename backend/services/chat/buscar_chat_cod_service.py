from repositories.chat_repository import ChatRepository

class BuscarChatCodService:
    def executar(self, id):
        chats = ChatRepository.buscar_chats(id)

        if not chats:
            return None

        return [chat.to_dict() for chat in chats]