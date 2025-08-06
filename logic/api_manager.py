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
    
    def generate_batch_questions(self) -> dict:
        """
        Gera um lote de 10 perguntas (4 fáceis, 3 médias, 3 difíceis) em um só request.
        Retorna dict com chaves 'facil', 'medio', 'dificil', cada uma contendo lista de objetos:
        { pergunta, opcoes, resposta, dica }
        """
        if not self.online:
            raise RuntimeError("Modo offline: não é possível gerar batch via API")
                    
        prompt = (
                    "Você é um sistema que gera perguntas para o jogo 'Show do Milhão'.\n"
                    "Gere um JSON VALIDO com três chaves: \"facil\", \"medio\", \"dificil\".\n"
                    "- \"facil\": lista de 4 perguntas de nível fácil.\n"
                    "- \"medio\": lista de 3 perguntas de nível médio.\n"
                    "- \"dificil\": lista de 3 perguntas de nível difícil.\n"
                    "Cada pergunta deve ser um objeto com:\n"
                    "  \"pergunta\": string,\n"
                    "  \"opcoes\": lista de 5 strings,\n"
                    "  \"resposta\": string (a correta),\n"
                    "  \"dica\": string (pista curta).\n"
                    "RETORNE SOMENTE O JSON VALIDO, sem texto adicional."
                )
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um gerador de perguntas de quiz para o jogo 'Show do Milhão'. "
                        "Sempre responda EXCLUSIVAMENTE com JSON válido, sem nenhum texto explicativo ou blocos de código Markdown. "
                        "O JSON deve ter exatamente as chaves 'pergunta', 'opcoes', 'resposta' e 'dica'."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=2000
            )

        content = response.choices[0].message.content.strip()
            
        # Remove blocos de código (```json … ```)
        if "}" in content:
            content = content[: content.rfind("}") + 1]

        try:
            batch = json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(f"Conteúdo inválido da API (batch truncado?): {content!r}")
            raise RuntimeError("Resposta da API não é JSON válido (talvez truncada)")
        
        logging.info(f"Batch recebido via API: chaves {list(batch.keys())}")
        return batch
