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
        
        opcoes = pergunta.get('opcoes', [])
        correta = pergunta.get('resposta')

        if tipo == 'dica':
            self.ajudas['dica'] = False
            dica = pergunta.get('dica', None)
            if dica:
                # retorna somente a dica, sem prefixo
                return True, dica
            else:
                return True, "Sem dica disponível"

        if tipo == 'pular':
            self.ajudas['pular'] = False
            return True, "Pergunta pulada."

        if tipo == 'eliminar':
            # Elimina 3 opções, deixando apenas a correta e mais uma aleatória
            self.ajudas['eliminar'] = False
            # Opções incorretas
            erradas = [o for o in opcoes if o != correta]
            # Seleciona uma errada para manter
            if len(erradas) > 1:
                manter = random.choice(erradas)
            else:
                manter = erradas[0] if erradas else None
            # Calcula as eliminadas: todas erradas menos a que será mantida
            eliminadas = [o for o in erradas if o != manter]
            return True, eliminadas  # retorna lista de eliminadas para UI processar

        return False, "Tipo de ajuda desconhecido."

    def estado_ajudas(self):
        return self.ajudas.copy()