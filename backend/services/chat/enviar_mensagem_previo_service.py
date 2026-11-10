import json
from google.genai import types #type: ignore
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from flask import current_app as app #type: ignore

from models.ia import client
from repositories.chat_repository import ChatRepository

class EnviarMensagemChatPrevio:
    def executar(self, chat_id, mensagem):

        if not chat_id or not mensagem:
            print("Error 400\n", chat_id, "\n", mensagem)
            raise ValueError("Elementos da função estão faltando.")

        status = ChatRepository.enviar_mensagem(chat_id, mensagem)

        if status != True:
            raise Exception("Erro ao enviar mensagem para o chat.")



        #Requisição para a IA
        models = app.config['GEMINI_API_MODELS']
        prompt = app.config['GEMINI_API_PROMPT']
        response = None

        def rodar_prompt(model_name):
            
            return client.models.generate_content(
                model = model_name,
                contents = mensagem,
                config = types.GenerateContentConfig(
                    system_instruction=prompt,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    max_output_tokens=200
                ))
            
        for model in models:
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(rodar_prompt, model)
                    response = future.result(timeout=20.0) # Timeout de 20 segundos

                if not response or not hasattr(response, 'text'):
                    break
            except TimeoutError:
                print(f"Timeout: O modelo {model} demorou demais.")

            except Exception as e:
                print(f"Falha ao enviar mensagem para o modelo {model}. Motivo: {e}")
                continue

        if not response:
            raise ValueError("Falha ao enviar mensagem para a assistente virtual.")

        message_ia = {
            "sender": "IA",
            "avatar": "IA",
            "type": "ia",
            "text": response.text
        }

        message = json.dumps(message_ia)

        status = ChatRepository.enviar_mensagem(chat_id, message)

        if status == True and response:
            return True
        else:
            raise Exception("Erro durante a execução.")