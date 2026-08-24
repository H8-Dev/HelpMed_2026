from models.arquivos_model import Arquivo

class CompartilharMedicoArquivo:
    def executar(self, arq_id, med_id):
        arquivo = Arquivo.buscar_arquivo(arq_id)
        if not arquivo:
            return None

        arquivo.atualizar(
            med_id=med_id
        )
        
        return arquivo.to_dict()