from .database import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Interger, primary_key=True, nullable=False)
    total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    last_update = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()