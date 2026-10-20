from .database import db

class Chat(db.Model):
    __tablename__ = "chat"

    chat_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dados = db.Column(db.JSON, nullable=False)
    c_pac_id = db.Column(db.String(14), db.ForeignKey("pacientes.cpf", ondelete='CASCADE'), nullable=False)
    c_med_id = db.Column(db.String(15), db.ForeignKey("medicos.crm"))
    last_update = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "dados": self.dados,
            "c_pac_id": self.c_pac_id,
            "c_med_id": self.c_med_id,
            "last_update": self.last_update
        }