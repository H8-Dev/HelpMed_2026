from .database import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    pag_id = db.Column(db.Integer, primary_key=True, nullable=False)
    total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    med_id = db.Column(db.String(15), db.ForeignKey("medicos.crm"), nullable=False)
    pac_id = db.Column(db.String(14), db.ForeignKey("pacientes.cpf"), nullable=False)
    data_hora = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()