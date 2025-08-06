import logging
from logic.question_manager import QuestionManager
from logic.help_manager import HelpManager

class GameLogic:
    def __init__(self):
        self.qm = QuestionManager()
        self.hm = HelpManager()
        self.niveis = ['facil'] * 4 + ['medio'] * 3 + ['dificil'] * 3
        self.current_index = 0
        self.respostas_certas = 0
        self.premios = [1000, 2000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        self.pergunta_atual_obj = None

    def iniciar_jogo(self):
        """Inicia novo jogo resetando estado, criando novos managers."""
        self.current_index = 0
        self.respostas_certas = 0
        self.pergunta_atual_obj = None
        self.qm = QuestionManager()
        self.hm = HelpManager()
        logging.info("Novo jogo iniciado.")

    def avancar_pergunta(self):
        """Busca e armazena a próxima pergunta para exibição."""
        if self.current_index < len(self.niveis):
            nivel = self.niveis[self.current_index]
            self.pergunta_atual_obj = self.qm.obter_pergunta(nivel)
            logging.info(f"Pergunta obtida (nível {nivel}): {self.pergunta_atual_obj['pergunta']}")
            return self.pergunta_atual_obj
        self.pergunta_atual_obj = None
        return None

    def verificar_resposta(self, resposta_usuario):
        """Verifica a resposta para a pergunta atualmente armazenada."""
        pergunta = self.pergunta_atual_obj
        if not pergunta:
            return False, "Jogo finalizado"

        correta = pergunta['resposta'].strip().lower() == resposta_usuario.strip().lower()
        if correta:
            self.respostas_certas += 1
            self.current_index += 1
            logging.info("Resposta correta.")
            return True, "Resposta correta!"
        else:
            logging.info("Resposta errada. Fim de jogo.")
            # Força fim de jogo
            self.current_index = len(self.niveis)
            return False, f"Errado! A resposta correta era: {pergunta['resposta']}"

    def usar_ajuda(self, tipo: str):
        """Aplica a ajuda solicitada à pergunta atual"""
        if not self.pergunta_atual_obj:
            return False, "Nenhuma pergunta disponível."
        ok, resultado = self.hm.usar_ajuda(tipo, self.pergunta_atual_obj)
        if tipo == 'pular' and ok:
            self.current_index += 1
        return ok, resultado

    def jogo_finalizado(self):
        return self.current_index >= len(self.niveis)

    def pontuacao_final(self):
        if self.respostas_certas == 0:
            return 0
        return self.premios[self.respostas_certas - 1]

    def ajudas_disponiveis(self):
        if not self.hm:
            return {}
        return self.hm.estado_ajudas()