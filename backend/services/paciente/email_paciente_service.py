from models.pacientes_model import Paciente
from flask_mail import Message #type: ignore
from smtplib import SMTPException
from models.mail import mail

class EmailPacienteService:
    def executar(self, cpf):

        paciente = Paciente.buscar_cpf(cpf)
        if not paciente:
            raise ValueError("Paciente não existe.")

        email = paciente.email
        try:
            mensagem = Message(subject="Uso dos Dados Sensíveis HelpMed", recipients=[email])
            mensagem.body = f"""Olá, {paciente.nome} {paciente.sobrenome}!
Por requisição sua estamos encaminhando a seguir um relatório completo de como utilizamos seus dados sensíveis para o funcionamento do nosso app.

1. FINALIDADE DOS DADOS COLETADOS
=========================================
CPF: Meio principal de identificação única de usuários individuais, utilizado estritamente para identificação pelo lado do servidor e nunca exibido no lado do cliente.
Nome e Sobrenome: Meios de identificação públicas no lado do usuário. Estes são os nomes que aparecem nos arquivos criados e chats para uma identificação mais fácil.
Email: Meio principal de comunicação para enviarmos informações requisitadas e atualizações sobre nossos termos de uso.

2. SEUS DIREITOS
=========================================
A qualquer momento que desejar você pode acessar a nossa página de configurações e deletar os dados da sua conta nos quais ficão salvos por até 2 anos dentro de nossa base dados por lei, porém todas informações, chats ou arquivos estarão desativadas.

Atenciosamente,
Equipe de Suporte e Administração da HelpMed.
@2026 HelpMed
"""
            mail.send(mensagem)
            return 
        except Exception as e:
            raise ValueError("Não foi possível enviar o email.", type="GENERIC")

        except SMTPException as e:
            raise ValueError("Falha de comunicação com o email.", type="SMTP")