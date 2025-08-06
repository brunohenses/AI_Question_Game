import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ResultUI(ttk.Frame):
    def __init__(self, master, pontuacao, stats, voltar_callback):
        super().__init__(master)
        self.master = master
        self.pontuacao = pontuacao
        self.stats = stats  # Espera dict com estatísticas de jogo
        self.voltar_callback = voltar_callback
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.criar_widgets()

    def criar_widgets(self):
        self.master.configure(bg='#0d1b2a')

        titulo = ttk.Label(self, text="Resultado Final", font=("Arial", 24, "bold"), bootstyle="info")
        titulo.pack(pady=10)

        lbl_pontuacao = ttk.Label(
            self,
            text=f"Você ganhou: {self.pontuacao}€",
            font=("Arial", 18),
            bootstyle="success"
        )
        lbl_pontuacao.pack(pady=10)

        # Exibe estatísticas adicionais, se houver
        if self.stats:
            stats_frame = ttk.Labelframe(self, text="Estatísticas do Jogo", bootstyle="secondary")
            stats_frame.pack(fill='x', pady=10)
            for chave, valor in self.stats.items():
                linha = ttk.Frame(stats_frame)
                linha.pack(fill='x', pady=2)
                ttk.Label(linha, text=f"{chave}:", width=20, anchor='w').pack(side='left')
                ttk.Label(linha, text=str(valor), anchor='w').pack(side='left')

        btn_novo = ttk.Button(self, text="Jogar Novamente", bootstyle="primary", command=self.voltar_callback)
        btn_novo.pack(side='left', padx=10, pady=20)

        btn_sair = ttk.Button(self, text="Sair", bootstyle="danger", command=self.master.quit)
        btn_sair.pack(side='right', padx=10, pady=20)
