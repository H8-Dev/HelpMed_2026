from .database import db

class Chat(db.Model):
    __tablename__ = "chat"

    chat_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dados = db.Column(db.JSON, nullable=False)
    med_id = db.Column(db.String(15), db.ForeignKey("medicos.crm"))
    pac_id = db.Column(db.String(14), db.ForeignKey("pacientes.cpf", ondelete='CASCADE'), nullable=False)
    last_update = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()