from .database import db

class Arquivo(db.Model):
    __tablename__ = "arquivos"

    arq_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    pac_id = db.Column(db.String(14), db.ForeignKey('pacientes.cpf'), nullable=False)
    med_id = db.Column(db.String(15), db.ForeignKey('medicos.crm'))
    last_update = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "arq_id": self.arq_id,
            "type": self.type,
            "url": self.url,
            "pac_id": self.pac_id,
            "med_id": self.med_id,
            "last_update": self.last_update
        }