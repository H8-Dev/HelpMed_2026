from models.arquivos_model import Arquivo

class BuscarArquivoPorId:
    def executar(self, arq_id):
        arquivo = Arquivo.buscar_arquivo(arq_id)

        if arquivo is None:
            return None

        return arquivo.to_dict()
        
