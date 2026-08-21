from repositories.arquivos_repository import ArquivoRepository

class BuscarArquivoPorPaciente:
    def executar(self, pac_id, med_id):
        arquivos = ArquivoRepository.buscar_arquivos_por_paciente_e_medico(pac_id, med_id)

        if not arquivos:
            return None

        return [arquivo.to_dict() for arquivo in arquivos]