from .database import db

class Medico(db.Model):
    __tablename__ = "medicos"

    crm = db.Column(db.String(9), primary_key=True, nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    formacao = db.Column(db.String(100), nullable=False)
    data_create = db.Column(db.TIMESTAMP, nullable=False)

    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def atualizar(self, senha=None, nome=None, sobrenome=None, email=None, formacao=None):
        if senha is not None:
            self.senha = senha
        if nome is not None:
            self.nome = nome
        if sobrenome is not None:
            self.sobrenome = sobrenome
        if email is not None:
            self.email = email
        if formacao is not None:
            self.formacao = formacao
        
        db.session.commit()

    def deletar(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def buscar_crm(crm):
        return Medico.query.filter_by(crm=crm).first()
    
    def to_dict(self):
        return {
            "crm": self.crm,
            "cpf": self.cpf,
            "senha": self.senha,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "email": self.email,
            "formacao": self.formacao,
            "data_create": self.data_create
        }