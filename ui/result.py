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

        # Título
        titulo = ttk.Label(self, text="Resultado Final", font=("Arial", 24, "bold"), bootstyle="info")
        titulo.pack(pady=10)

        # Pontuação
        score_lbl = ttk.Label(
            self, text=f"Você ganhou: {self.pontuacao}€",
            font=("Arial", 18, "bold"), bootstyle="success"
        )
        score_lbl.pack(pady=10)

        # Divider
        sep = ttk.Separator(self, orient='horizontal')
        sep.pack(fill='x', pady=10)

        # Estatísticas resumidas
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill='x', pady=5)

        # Perguntas respondidas
        perguntas = self.stats.get("Perguntas Respondidas", 0)
        lbl_perg = ttk.Label(
            stats_frame, text=f"Perguntas Respondidas: {perguntas}",
            font=("Arial", 12, "bold")
        )
        lbl_perg.pack(anchor='w', pady=2)

        # Ajuda usadas
        ajudas_usadas = self.stats.get("Ajudas Restantes", {})
        used = [k.capitalize() for k, available in ajudas_usadas.items() if not available]
        if used:
            # Mapeia ícones simples
            icons = {'Pular': '🏃', 'Dica': '💡', 'Eliminar': '✂️'}
            lbl_ajudas = ttk.Label(
                stats_frame,
                text="Ajudas usadas: " + ", ".join(f"{icons.get(a, '')} {a}" for a in used),
                font=("Arial", 12, "bold")
            )
            lbl_ajudas.pack(anchor='w', pady=2)
        else:
            lbl_ajudas = ttk.Label(
                stats_frame, text="Nenhuma ajuda utilizada.",
                font=("Arial", 12, "bold")
            )
            lbl_ajudas.pack(anchor='w', pady=2)

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        btn_novo = ttk.Button(
            btn_frame, text="Jogar Novamente",
            bootstyle="primary", command=self.voltar_callback
        )
        btn_novo.grid(row=0, column=0, padx=10)

        btn_sair = ttk.Button(
            btn_frame, text="Sair",
            bootstyle="danger", command=self.master.quit
        )
        btn_sair.grid(row=0, column=1, padx=10)

        # Ajusta background dos filhos
        for child in self.winfo_children():
            try:
                child.configure(background='#0d1b2a')
            except:
                pass
    
    def destroy(self):
        # Limpa dica e status antes de descartar
        super().destroy()

