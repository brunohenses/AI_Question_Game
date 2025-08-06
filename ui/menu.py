import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MenuUI(ttk.Frame):
    def __init__(self, master, iniciar_callback):
        super().__init__(master)
        self.master = master
        self.iniciar_callback = iniciar_callback
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.criar_widgets()

    def criar_widgets(self):
        titulo = ttk.Label(self, text="Show do Milhão", font=("Arial", 28, "bold"))
        titulo.pack(pady=30)

        descricao = ttk.Label(
            self,
            text="Responda 10 perguntas e tente ganhar o prêmio máximo!",
            font=("Arial", 14),
        )
        descricao.pack(pady=10)

        btn_iniciar = ttk.Button(self, text="Iniciar Jogo", bootstyle="success", command=self.iniciar_callback)
        btn_iniciar.pack(pady=10)

        btn_sair = ttk.Button(self, text="Sair", bootstyle="danger", command=self.master.quit)
        btn_sair.pack(pady=10)

        creditos = ttk.Label(
            self,
            text="Desenvolvido em Python com Tkinter + TTKBootstrap por Bruno Henses",
            font=("Arial", 10),
            foreground="gray",
        )
        creditos.pack(side="bottom", pady=10)