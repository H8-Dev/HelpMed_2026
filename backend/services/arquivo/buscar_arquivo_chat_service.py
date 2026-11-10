from repositories.arquivos_repository import ArquivoRepository

class BuscarArquivoPorChat:
    def executar(self, chat_id):
        arquivos = ArquivoRepository.buscar_arquivos_por_chat(chat_id)

        if not arquivos:
            return None

        return [arquivo.to_dict() for arquivo in arquivos]