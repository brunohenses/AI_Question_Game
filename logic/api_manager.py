import openai
import logging
import json
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

class APIManager:
    def __init__(self):
        if not OPENAI_API_KEY:
            self.onine = False
            logging.info("APIManager: Modo offline. Não serão feitas chamadas à OpenAI")
        else:
            self.online = True
            openai.api_key = OPENAI_API_KEY
            logging.info("APIManager: Chave da OpenAI carregada com sucesso.")
    
    def generate_question(self, nivel:str) -> dict:
        """
        Gera uma pewrgunta de quiz via OpenAI
        retorna dict com 'pergunta', 'opcoes', 'resposta' e 'dica'
        """
        if not self.online:
            raise RuntimeError("Tentativa de gerar pergunta em modo offline.")
        
        prompt = (
            f"Gere uma pergunta de quiz de nível {nivel} para um jogo no estilo 'Show do Milhão'. "
            "A resposta correta deve estar entre 5 opções. Inclua também uma dica que ajude o jogador a pensar na resposta.\n"
            "Retorne SOMENTE um JSON com os seguintes campos: \n"
            "- pergunta (string), \n"
            "- opcoes (lista de 5 strings), \n"
            "- resposta (string correta), \n"
            "- dica (string curta com uma pista)."
        )

        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
            )
            content = response.choices[0].message.content
            question_dict = json.loads(content)
            logging.info(f"Pergunta gerada (nivel {nivel}): {question_dict['pergunta']}.")
            return question_dict
        except Exception as e:
            logging.error(f"Erro ao gerar perguntavia API: {e}")
            raise