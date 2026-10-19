from repositories.arquivos_repository import ArquivoRepository

class BuscarArquivoPorUser():
    def executar(self, id):
        arquivos = ArquivoRepository.buscar_arquivo_por_user(id)

        if not arquivos:
            return None

        return [arquivo.to_dict() for arquivo in arquivos]
    