import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from logic.game_logic import GameLogic

class GameUI(ttk.Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master)
        self.master = master
        self.voltar_callback = voltar_callback
        self.game = GameLogic()
        self.pack(fill=BOTH, expand=True)
        self._criar_widgets()

    def _criar_widgets(self):
        self.master.configure(bg='#0d1b2a')
        # Prize display
        self.lbl_premio = ttk.Label(self, text='Prêmio Atual: 0', font=('Arial', 16), bootstyle='info')
        self.lbl_premio.pack(pady=10)

        # Pergunta
        self.lbl_pergunta = tk.Label(self, text='', wraplength=600, fg='white', bg='#1b263b', font=('Arial', 18, 'bold'))
        self.lbl_pergunta.pack(pady=20, fill='x')

        # Label dedicado para dicas abaixo da pergunta
        self.lbl_dica = ttk.Label(self, text='', font=('Arial', 12, 'italic'), bootstyle='warning')
        self.lbl_dica.pack(pady=(0, 15))

        # Opções
        self.opcoes_frame = ttk.Frame(self)
        self.opcoes_frame.pack(pady=10)
        self.btn_opcoes = []
        for i in range(5):
            btn = ttk.Button(self.opcoes_frame, text=f'Opção {i+1}', bootstyle='primary', command=lambda idx=i: self._responder(idx))
            btn.grid(row=i, column=0, sticky='ew', pady=5)
            self.btn_opcoes.append(btn)

        # Ações: parar e ajuda
        acoes_frame = ttk.Frame(self)
        acoes_frame.pack(pady=20)
        self.btn_parar = ttk.Button(acoes_frame, text='Parar', bootstyle='warning', command=self._parar)
        self.btn_parar.grid(row=0, column=0, padx=10)
        self.btn_ajuda = ttk.Menubutton(acoes_frame, text='Ajuda', bootstyle='secondary')
        self.menu_ajuda = tk.Menu(self.btn_ajuda, tearoff=0)
        # Adiciona opções de ajuda com índices
        self.menu_ajuda.add_command(label='Dica', command=lambda: self._usar_ajuda('dica'))
        self.menu_ajuda.add_command(label='Pular', command=lambda: self._usar_ajuda('pular'))
        self.menu_ajuda.add_command(label='Eliminar', command=lambda: self._usar_ajuda('eliminar'))
        self.btn_ajuda['menu'] = self.menu_ajuda
        self.btn_ajuda.grid(row=0, column=1, padx=10)

        # Feedback
        self.lbl_status = ttk.Label(self, text='', font=('Arial', 14), bootstyle='light')
        self.lbl_status.pack(pady=10)

        # Botão de voltar ao menu
        self.btn_voltar = ttk.Button(self, text='Voltar ao Menu', bootstyle='danger', command=self.voltar_callback)
        self.btn_voltar.pack(side='bottom', pady=10)

        # Inicia jogo
        self.game.iniciar_jogo()
        self._atualizar_tela()

    def _atualizar_tela(self):
        # Limpa dica da pergunta anterior
        self.lbl_dica.config(text='')
        
        pergunta = self.game.obter_pergunta_atual()
        if not pergunta:
            self._encerrar_jogo(final=True)
            return

        # Atualiza prêmio
        self.lbl_premio.config(text=f'Prêmio Atual: {self.game.pontuacao_final()}')
        # Atualiza pergunta e opções
        self.lbl_pergunta.config(text=pergunta['pergunta'])
        for idx, opc in enumerate(pergunta['opcoes']):
            self.btn_opcoes[idx].config(text=opc, state='normal')
        # Atualiza estado de ajudas
        for label in ['Dica', 'Pular', 'Eliminar']:
            state = 'normal'
            tipo = 'dica' if label=='Dica' else ('pular' if label=='Pular' else 'eliminar')
            if not self.game.ajudas_disponiveis().get(tipo):
                state = 'disabled'
            self.menu_ajuda.entryconfig(label, state=state)
        self.btn_parar.state(['!disabled'])
        self.btn_ajuda.state(['!disabled'])
        self.lbl_status.config(text='')

    def _responder(self, idx):
        # Impede múltiplas tentativas na mesma pergunta
        for btn in self.btn_opcoes:
            btn.state(['disabled'])
        opc = self.btn_opcoes[idx].cget('text')
        certo, msg = self.game.verificar_resposta(opc)
        self.lbl_status.config(text=msg)
        if not certo:
            self._encerrar_jogo()
        else:
            self._atualizar_tela()

    def _parar(self):
        pontos = self.game.pontuacao_final()
        self.lbl_status.config(text=f'Você parou com: {pontos}')
        self._encerrar_jogo()

    def _usar_ajuda(self, tipo):
        ok, resultado = self.game.usar_ajuda(tipo)
        # resultado é string para dica/pular, ou lista de eliminadas para 'eliminar'

        # 1) Exibe a mensagem correta: dica ou texto de pular
        if tipo == 'dica' and ok:
            # Atualiza label de dica
            self.lbl_dica.config(text=resultado)
            # Desabilita menu
            self.menu_ajuda.entryconfig('Dica', state='disabled')
            return
        elif tipo == 'pular' and ok:
            self.lbl_status.config(text=resultado)
            # Avança imediatamente para a próxima pergunta
            self._atualizar_tela()
        elif tipo == 'eliminar' and ok:
            # 'resultado' é lista de opções a desabilitar
            for btn in self.btn_opcoes:
                if btn.cget('text') in resultado:
                    btn.state(['disabled'])
            self.lbl_status.config(text='Opções eliminadas')
        else:
            # Caso não aprovou ou tipo inválido
            self.lbl_status.config(text=resultado)

        # 2) Desabilita o item do menu de ajuda
        if tipo == 'Dica':
            self.menu_ajuda.entryconfig('Dica', state='disabled')
        elif tipo == 'Pular':
            self.menu_ajuda.entryconfig('Pular', state='disabled')
        elif tipo == 'Eliminar':
            self.menu_ajuda.entryconfig('eliminar', state='disabled')

        # 3) Se for 'eliminar' e ok, desabilita os botões correspondentes
        if tipo == 'eliminar' and ok:
            # 'resultado' é a lista de textos eliminados
            for btn in self.btn_opcoes:
                if btn.cget('text') in resultado:
                    btn.state(['disabled'])

        # 4) Se a ajuda for pular, atualiza a tela imediatamente
        if tipo == 'pular' and ok:
            self._atualizar_tela()

    def _encerrar_jogo(self, final=False):
        # Desabilita todas ações após fim ou erro
        for btn in self.btn_opcoes:
            btn.state(['disabled'])
        self.btn_parar.state(['disabled'])
        self.btn_ajuda.state(['disabled'])
        if final:
            self.lbl_status.config(text=f'Fim de jogo! Você ganhou: {self.game.pontuacao_final()}')

