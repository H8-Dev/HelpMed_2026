from .database import db

class Arquivo(db.Model):
    __tablename__ = "arquivos"

    arq_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    nome_arq = db.Column(db.String(100), nullable=False)
    dados = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    pac_id = db.Column(db.String(14), db.ForeignKey('pacientes.cpf', ondelete='CASCADE'), nullable=False)
    med_id = db.Column(db.String(15), db.ForeignKey('medicos.crm'))
    last_update = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self, type=None, nome_arq=None, dados=None, med_id=None, last_update=None):
        if type is not None:
            self.type = type
        if nome_arq is not None:
            self.nome_arq = nome_arq
        if dados is not None:
            self.dados = dados
        if med_id is not None:
            self.med_id = med_id
        if last_update is not None:
            self.last_update = last_update

        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def buscar_arquivo(arq_id):
        return Arquivo.query.filter_by(arq_id=arq_id).first()

    def to_dict(self):
        return {
            "arq_id": self.arq_id,
            "type": self.type,
            "nome_arq": self.nome_arq,
            "dados": self.dados,
            "pac_id": self.pac_id,
            "med_id": self.med_id,
            "last_update": self.last_update
        }