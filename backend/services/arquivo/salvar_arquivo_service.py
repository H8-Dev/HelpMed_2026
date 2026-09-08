from datetime import datetime
from models.arquivos_model import Arquivo

class SalvarArquivoService:
    def salvar(self, dados):
        required = ["type", "nome_arq", "dados", "pac_id"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")

        arquivo = Arquivo(
            type = dados["type"],
            nome_arq = dados["nome_arq"],
            dados = dados["dados"],
            pac_id = dados["pac_id"],
            med_id = dados["med_id"] or None,
            last_update = datetime.now()
        )

        arquivo.salvar()
        return arquivo.to_dict()