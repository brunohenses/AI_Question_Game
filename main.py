import tkinter as tk
import ttkbootstrap as ttk
from ui.menu import MenuUI
from ui.game import GameUI
from ui.result import ResultUI

class App:
    def __init__(self, root):
        self.root = root
        root.title("Show do Milhão")
        self.style = ttk.Style(theme="litera")
        self.menu = MenuUI(root, iniciar_callback=self.iniciar_jogo)
        self.game = None
        self.result = None

    def iniciar_jogo(self):
        self.menu.destroy()
        self.game = GameUI(self.root, voltar_callback=self.voltar_menu)

    def voltar_menu(self):
        # Se veio da tela de jogo: se ainda não finalizou, destrói game
        if self.game:
            # Coleta estatísticas antes de destruir
            pontuacao = self.game.game.pontuacao_final()
            stats = {
                "Perguntas Respondidas": self.game.game.respostas_certas,
                "Ajudas Restantes": self.game.game.ajudas_disponiveis()
            }
            self.game.destroy()
        else:
            pontuacao = 0
            stats = {}
        # Exibe resultado
        self.result = ResultUI(self.root, pontuacao=pontuacao, stats=stats, voltar_callback=self.resetar)

    def resetar(self):
        if self.result:
            self.result.destroy()
        self.menu = MenuUI(self.root, iniciar_callback=self.iniciar_jogo)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
