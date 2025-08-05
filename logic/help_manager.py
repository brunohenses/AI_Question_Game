import random

class HelpManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.ajudas = {
            'pular': True,
            'dica': True,
            'eliminar': True
        }

    def pode_usar(self, tipo):
        return self.ajudas.get(tipo, False)

    def usar_ajuda(self, tipo, pergunta: dict):
        if not self.pode_usar(tipo):
            return False, "Ajuda já utilizada ou inválida."

        if tipo == 'dica':
            self.ajudas['dica'] = False
            return True, f"Dica: {pergunta.get('dica', 'Sem dica disponível')}"

        if tipo == 'pular':
            self.ajudas['pular'] = False
            return True, "Pergunta pulada."

        if tipo == 'eliminar':
            opcoes = pergunta['opcoes']
            correta = pergunta['resposta']
            erradas = [o for o in opcoes if o != correta]
            eliminadas = random.sample(erradas, 2)
            self.ajudas['eliminar'] = False
            return True, f"Opções eliminadas: {', '.join(eliminadas)}"

        return False, "Tipo de ajuda desconhecido."

    def estado_ajudas(self):
        return self.ajudas.copy()