import tkinter as tk
import random
import cores

class Jogo(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)  # construtor do Tkinter para inicializar a janela
        self.grid()  # organiza os widgets dentro da janela
        self.master.title('2048')  # título da janela

        # Aqui, está sendo criado um quadro principal dentro da janela e colocando na grade principal
        self.grade_principal = tk.Frame(
            self, bg=cores.COR_GRADE, bd=3, width=400, height=400) 
        self.grade_principal.grid(pady=(80, 0)) 

        # cria a interface gráfica e inicia o jogo
        self.criar_Interface()
        self.start_game()

        # controla o movimento das peças 
        self.master.bind("<Left>", self.esquerda)
        self.master.bind("<Right>", self.direita)
        self.master.bind("<Up>", self.cima)
        self.master.bind("<Down>", self.baixo)

        # Mantém o jogo aberto até que a janela seja fechada
        self.mainloop()

    def criar_Interface(self):
        self.celulas = []
        for i in range(4):
            linha = []
            for j in range(4):
                quadrado_celula = tk.Frame(
                    self.grade_principal,
                    bg=cores.COR_CELULA_VAZIA,
                    width=100,
                    height=100)
                quadrado_celula.grid(row=i, column=j, padx=5, pady=5)
                numero_da_celula = tk.Label(self.grade_principal, bg=cores.COR_CELULA_VAZIA)
                numero_da_celula.grid(row=i, column=j)
                celula = {"frame": quadrado_celula, "number": numero_da_celula}
                linha.append(celula)
            self.celulas.append(linha)

        frame_do_score = tk.Frame(self)
        frame_do_score.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            frame_do_score,
            text="Score",
            font=cores.FONTE_ROTULO_PONTUACAO).grid(
            row=0)
        self.legenda_score = tk.Label(frame_do_score, text="0", font=cores.FONTE_PONTUACAO)
        self.legenda_score.grid(row=1)

    def start_game(self):
        self.matriz = [[0] * 4 for _ in range(4)]

        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matriz[row][col] = 2

        self.celulas[row][col]["frame"].configure(bg=cores.CORES_CELULA[2])
        self.celulas[row][col]["number"].configure(
            bg=cores.CORES_CELULA[2],
            fg=cores.CORES_NUMERO_CELULA[2],
            font=cores.FONTE_NUMERO_CELULA[2],
            text="2")

        while(self.matriz[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matriz[row][col] = 2

        self.celulas[row][col]["frame"].configure(bg=cores.CORES_CELULA[2])
        self.celulas[row][col]["number"].configure(
            bg=cores.CORES_CELULA[2],
            fg=cores.CORES_NUMERO_CELULA[2],
            font=cores.FONTE_NUMERO_CELULA[2],
            text="2")

        self.score = 0
        self.jogadas = 0

        # self.add_2048_win()
        # self.add_defeat()


    def empilhar(self):
        nova_matriz = [[0] * 4 for _ in range(4)]
        for row in range(4):
            posicao_preenchida = 0
            for col in range(4):
                if self.matriz[row][col] != 0:
                    nova_matriz[row][posicao_preenchida] = self.matriz[row][col]
                    posicao_preenchida += 1
        self.matriz = nova_matriz

    def combinar(self):
        for row in range(4):
            for col in range(3):
                if self.matriz[row][col] != 0 and self.matriz[row][col] == self.matriz[row][col + 1]:
                    self.matriz[row][col] *= 2
                    self.matriz[row][col + 1] = 0
                    self.score += self.matriz[row][col]

    def reverter(self):
        nova_matriz = []
        for row in range(4):
            nova_matriz.append([])
            for col in range(4):
                nova_matriz[row].append(self.matriz[row][3 - col])
        self.matriz = nova_matriz

    def transpor(self):
        nova_matriz = [[0] * 4 for _ in range(4)]
        for row in range(4):
            for col in range(4):
                nova_matriz[row][col] = self.matriz[col][row]
        self.matriz = nova_matriz

    def add_nova_peca(self):
        if any(0 in row for row in self.matriz):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while(self.matriz[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            if random.random() < 0.9:
                self.matriz[row][col] = 2
            else:
                self.matriz[row][col] = 4

    def atualizar_Interface(self):
        for i in range(4):
            for j in range(4):
                valor_da_celula = self.matriz[i][j]
                if valor_da_celula == 0:
                    self.celulas[i][j]["frame"].configure(bg=cores.COR_CELULA_VAZIA)
                    self.celulas[i][j]["number"].configure(
                        bg=cores.COR_CELULA_VAZIA, text="")
                else:
                    self.celulas[i][j]["frame"].configure(
                        bg=cores.CORES_CELULA[valor_da_celula])
                    self.celulas[i][j]["number"].configure(
                        bg=cores.CORES_CELULA[valor_da_celula],
                        fg=cores.CORES_NUMERO_CELULA[valor_da_celula],
                        font=cores.FONTE_NUMERO_CELULA[valor_da_celula],
                        text=str(valor_da_celula))
        self.legenda_score.configure(text=self.score)
        self.update_idletasks()

    def esquerda(self, event):
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        # self.add_defeat()
        self.fim_de_jogo()

    def direita(self, event):
        self.reverter()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.reverter()
        self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def cima(self, event):
        self.transpor()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.transpor()
        self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def baixo(self, event):
        self.transpor()
        self.reverter()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.reverter()
        self.transpor()
        self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    # def add_2048_win(self):
    #     empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matriz[i][j] == 0]
        
    #     if empty_cells:
    #         row, col = random.choice(empty_cells)
    #         self.matriz[row][col] = 2048

    # def add_defeat(self):
    #     self.matriz[0] = [2, 4, 8, 16]
    #     self.matriz[1] = [32, 64, 128, 256]
    #     self.matriz[2] = [512, 1024, 2, 4]
    #     self.matriz[3] = [8, 16, 32, 64]

    def existe_mov_horizontal(self):
        for row in range(4):
            for col in range(3):
                if self.matriz[row][col] == self.matriz[row][col + 1]:
                    return True
        return False

    def existe_mov_vertical(self):
        for row in range(3):
            for col in range(4):
                if self.matriz[row][col] == self.matriz[row + 1][col]:
                    return True
        return False
    
    def mostra_jogadas_e_recorde(self):
        # Mostra o Score Final
        frame_pontuacao = tk.Frame(self.grade_principal, borderwidth=2)
        frame_pontuacao.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(
            frame_pontuacao,
            text=f"Score: {self.score}",
            bg=cores.FUNDO_PONTUACAO,
            fg=cores.COR_FONTE_FIM_DE_JOGO,
            font=cores.FONTE_PONTUACAO).pack()
        
        # Mostra a quantidade de jogadas
        frame_jogadas = tk.Frame(self.grade_principal, borderwidth=2)
        frame_jogadas.place(relx=0.5, rely=0.6, anchor="center")
        tk.Label(
            frame_jogadas,
            text=f"Jogadas: {self.jogadas}",
            bg=cores.FUNDO_JOGADAS_RECORDE,
            fg=cores.COR_FONTE_FIM_DE_JOGO,
            font=cores.FONTE_JOGADAS_RECORDE).pack()
        
        # Mostra o recorde
        frame_recorde = tk.Frame(self.grade_principal, borderwidth=2)
        frame_recorde.place(relx=0.5, rely=0.7, anchor="center")
        tk.Label(
            frame_recorde,
            text=f"Recorde: {self.ler_recorde()}",
            bg=cores.FUNDO_JOGADAS_RECORDE,
            fg=cores.COR_FONTE_FIM_DE_JOGO,
            font=cores.FONTE_JOGADAS_RECORDE).pack()
        
    def ler_recorde(self):
        try:
            with open("recorde.txt", "r") as arquivo:
                recorde = int(arquivo.read())
            return recorde
        except FileNotFoundError:
            recorde = 0
            with open("recorde.txt", "w") as arquivo:
                arquivo.write(str(recorde))
            return recorde
        
    def verifica_recorde(self):
        recorde = self.ler_recorde()
        
        if self.score > recorde:
            with open("recorde.txt", "w") as arquivo:
                arquivo.write(str(self.score))


    def fim_de_jogo(self):
        if any(2048 in row for row in self.matriz):
            frame_fim_de_jogo = tk.Frame(self.grade_principal, borderwidth=2)
            frame_fim_de_jogo.place(relx=0.5, rely=0.20, anchor="center")
            tk.Label(
                frame_fim_de_jogo,
                text="VITÓRIA!",
                bg=cores.FUNDO_VENCEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
            self.verifica_recorde()
            self.mostra_jogadas_e_recorde()
        elif not any(0 in row for row in self.matriz) and not self.existe_mov_horizontal() and not self.existe_mov_vertical():
            frame_fim_de_jogo = tk.Frame(self.grade_principal, borderwidth=2)
            frame_fim_de_jogo.place(relx=0.5, rely=0.20, anchor="center")
            tk.Label(
                frame_fim_de_jogo,
                text="DERROTA!",
                bg=cores.FUNDO_PERDEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
            self.verifica_recorde()
            self.mostra_jogadas_e_recorde()

Jogo()