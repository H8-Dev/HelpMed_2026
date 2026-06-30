from .database import db

class Paciente(db.Model):
    __tablename__ = "pacientes"

    cpf = db.Column(db.String(14), primary_key=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    data_create = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self, senha=None, nome=None, sobrenome=None, email=None):
        if senha is not None:
            self.senha = senha
        if nome is not None:
            self.nome = nome
        if sobrenome is not None:
            self.sobrenome = sobrenome
        if email is not None:
            self.email = email
        
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()