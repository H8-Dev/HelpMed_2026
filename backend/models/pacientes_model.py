from .database import db
import re

class Paciente(db.Model):
    __tablename__ = "pacientes"

    cpf = db.Column(db.String(14), primary_key=True, nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)
    data_create = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self, senha=None, nome=None, sobrenome=None, email=None, ativo=None):
        if senha is not None:
            self.senha = senha
        if nome is not None:
            self.nome = nome
        if sobrenome is not None:
            self.sobrenome = sobrenome
        if email is not None:
            self.email = email
        if ativo is not None:
            self.ativo = ativo
        
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def buscar_cpf(cpf):
        if "." not in str(cpf):
            cpf = str(cpf).zfill(11)
            cpf = re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", cpf)
            return Paciente.query.filter_by(cpf=cpf).first()

        return Paciente.query.filter_by(cpf=cpf).first()

    @staticmethod
    def buscar_email(email):
        return Paciente.query.filter_by(email=email).first()

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "senha": self.senha,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "email": self.email
        }