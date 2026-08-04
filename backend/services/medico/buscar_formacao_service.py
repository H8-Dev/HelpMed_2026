from models.medico_model import Medico

class BuscarMedicoPorFormacaoService:
    def executar(self, formacao):
        medicos = Medico.buscar_formacao(formacao)

        if not medicos:
            return None

        return [medico.to_dict() for medico in medicos]