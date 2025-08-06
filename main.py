import tkinter as tk
import ttkbootstrap as ttk
from ui.menu import MenuUI
from ui.game import GameUI
from ui.result import ResultUI
from logic.stats_manager import StatsManager

class App:
    def __init__(self, root):
        self.root = root
        root.title("Show do Milhão")
        self.style = ttk.Style(theme="litera")
        self.menu = MenuUI(root, iniciar_callback=self.iniciar_jogo)
        self.game = None
        self.result = None
        self.stats_mgr = StatsManager()

    def iniciar_jogo(self):
        self.menu.destroy()
        self.game = GameUI(self.root, voltar_callback=self.voltar_menu)

    def voltar_menu(self):
        if self.game:
            # 1) Coleta estatísticas antes de destruir a UI do jogo
            perguntas_resp = self.game.game.respostas_certas
            ajudas_usadas = {k: not v for k, v in self.game.game.ajudas_disponiveis().items()}
            pontuacao = self.game.game.pontuacao_final()

            # 2) Registra no stats.json
            self.stats_mgr.add_record(
                perguntas_respondidas=perguntas_resp,
                ajudas_usadas=ajudas_usadas,
                pontuacao=pontuacao
            )

            # 3) Destrói a tela de jogo
            self.game.destroy()
        else:
            # Se não havia jogo em curso
            perguntas_resp = 0
            ajudas_usadas = {}
            pontuacao = 0

        stats = {
            "Perguntas Respondidas": perguntas_resp,
            "Ajudas Restantes": self.game.game.ajudas_disponiveis() if self.game else {}
        }

        # 4) Exibe tela de resultado
        self.result = ResultUI(
            self.root,
            pontuacao=pontuacao,
            stats=stats,
            voltar_callback=self.resetar
        )

    def resetar(self):
        if self.result:
            self.result.destroy()
        self.menu = MenuUI(self.root, iniciar_callback=self.iniciar_jogo)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
