from models.medico_model import Medico
from flask_mail import Message #type: ignore
from smtplib import SMTPException
from models.mail import mail


class EmailMedicoService:
    def executar(crm):

        medico = Medico.buscar_crm(crm)
        if not medico:
            raise ValueError("Médico não existe.")
        email = medico.email
        try:
            mensagem = Message(subject="Uso dos Dados Sensíveis HelpMed", recipients=[email])
            mensagem.body = f"""Olá, {medico.nome} {medico.sobrenome}!
Por requisição sua estamos encaminhando a seguir um relatório completo de como utilizamos seus dados sensíveis para o funcionamento do nosso app.

1. FINALIDADE DOS DADOS COLETADOS
=========================================
CRM: Meio principal de identificação única dos médicos cadastrados na HelpMed, utilizado estritamente para identificação pelo lado do servidor e nunca exibido no lado do cliente.
CPF: Meio principal de identificação única de usuários individuais, utilizado para validar o CRM utilizado certificando que o médico é uma pessoa física.
Nome e Sobrenome: Meios de identificação públicas no lado do usuário. Estes são os nomes que aparecem nos arquivos criados e chats para uma identificação mais fácil.
Email: Meio principal de comunicação para enviarmos informações requisitadas e atualizações sobre nossos termos de uso.
Formação: Dado qualificante para o direcionamento de novos pacientes a médicos qualificados a ajudá-los.

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