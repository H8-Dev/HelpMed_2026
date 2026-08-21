from repositories.medicos_repository import MedicosRepository

class BuscarMedicoPorFormacaoService:
    def executar(self, formacao):
        medicos = MedicosRepository.buscar_formacao(formacao)

        if not medicos:
            return None

        return [medico.to_dict() for medico in medicos]