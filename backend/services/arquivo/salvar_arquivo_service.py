from datetime import datetime
from models.arquivos_model import Arquivo

class SalvarArquivoService:
    def salvar(self, dados):
        required = ["type", "url", "pac_id"]

        for item in required:
            if not dados.get(item):
                raise ValueError(f"O campo {item} é obrigatório!")

        arquivo = Arquivo(
            type = dados["type"],
            url = dados["url"],
            pac_id = dados["pac_id"],
            med_id = dados["med_id"] or None,
            last_update = datetime.now()
        )

        arquivo.salvar()
        return arquivo.to_dict()