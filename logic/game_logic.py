import logging
from logic.question_manager import QuestionManager
from logic.help_manager import HelpManager

class GameLogic:
    def __init__(self):
        self.qm = QuestionManager()
        self.hm = HelpManager()
        self.niveis = ['facil'] * 4 + ['media'] * 3 + ['dificil'] * 3
        self.perguntas = []
        self.respostas_certas = 0
        self.premios = [100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 100000]
        self.pergunta_atual = 0

    def iniciar_jogo(self):
        self.perguntas = [self.qm.obter_pergunta(nivel) for nivel in self.niveis]
        self.pergunta_atual = 0
        self.respostas_certas = 0
        self.hm.reset()
        logging.info("Novo jogo iniciado.")

    def obter_pergunta_atual(self):
        if self.pergunta_atual < len(self.perguntas):
            return self.perguntas[self.pergunta_atual]
        return None

    def verificar_resposta(self, resposta_usuario):
        pergunta = self.obter_pergunta_atual()
        if not pergunta:
            return False, "Jogo finalizado"

        correta = pergunta['resposta'].strip().lower() == resposta_usuario.strip().lower()
        if correta:
            self.respostas_certas += 1
            self.pergunta_atual += 1
            logging.info("Resposta correta.")
            return True, "Resposta correta!"
        else:
            logging.info("Resposta errada. Fim de jogo.")
            return False, f"Errado! A resposta correta era: {pergunta['resposta']}"

    def usar_ajuda(self, tipo):
        pergunta = self.obter_pergunta_atual()
        if not pergunta:
            return False, "Nenhuma pergunta disponível."

        resultado, mensagem = self.hm.usar_ajuda(tipo, pergunta)
        if tipo == 'pular' and resultado:
            self.pergunta_atual += 1
        return resultado, mensagem

    def jogo_finalizado(self):
        return self.pergunta_atual >= len(self.perguntas)

    def pontuacao_final(self):
        if self.respostas_certas == 0:
            return 0
        return self.premios[self.respostas_certas - 1]

    def ajudas_disponiveis(self):
        return self.hm.estado_ajudas()