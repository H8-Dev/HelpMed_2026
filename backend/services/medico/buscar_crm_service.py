from models.medico_model import Medico

class BuscarMedicoPorCRMService:
    def executar(self, medico_crm):
        medico = Medico.buscar_crm(medico_crm)

        if medico is None:
            return None

        return medico.to_dict()