import tkinter as tk
import random
import cores

score = 0

class Jogo(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)  # construtor do Tkinter para inicializar a janela
        self.grid()  # organiza os widgets dentro da janela
        self.master.title('2048')  # título da janela

        # Aqui, está sendo criado um quadro principal dentro da janela e colocando na grade principal
        self.main_grid = tk.Frame(
            self, bg=cores.COR_GRADE, bd=3, width=400, height=400) 
        self.main_grid.grid(pady=(80, 0)) 

        # cria a interface gráfica e inicia o jogo
        self.criar_Interface()
        self.start_game()

        # controlar o movimento das peças 
        self.master.bind("<Left>", self.esquerda)
        self.master.bind("<Right>", self.direita)
        self.master.bind("<Up>", self.cima)
        self.master.bind("<Down>", self.baixo)

        # Mantém o jogo aberto até que a janela seja fechada
        self.mainloop()


    def criar_Interface(self):
        self.celulas = []
        for i in range(4):
            row = []
            for j in range(4):
                quadrado_celula = tk.Frame(
                    self.main_grid,
                    bg=cores.COR_CELULA_VAZIA,
                    width=100,
                    height=100)
                quadrado_celula.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=cores.COR_CELULA_VAZIA)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": quadrado_celula, "number": cell_number}
                row.append(cell_data)
            self.celulas.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=cores.FONTE_ROTULO_PONTUACAO).grid(
            row=0)
        self.score_label = tk.Label(score_frame, text="0", font=cores.FONTE_PONTUACAO)
        self.score_label.grid(row=1)

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
                cell_value = self.matriz[i][j]
                if cell_value == 0:
                    self.celulas[i][j]["frame"].configure(bg=cores.COR_CELULA_VAZIA)
                    self.celulas[i][j]["number"].configure(
                        bg=cores.COR_CELULA_VAZIA, text="")
                else:
                    self.celulas[i][j]["frame"].configure(
                        bg=cores.CORES_CELULA[cell_value])
                    self.celulas[i][j]["number"].configure(
                        bg=cores.CORES_CELULA[cell_value],
                        fg=cores.CORES_NUMERO_CELULA[cell_value],
                        font=cores.FONTE_NUMERO_CELULA[cell_value],
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def esquerda(self, event):
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def direita(self, event):
        self.reverter()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.reverter()
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def cima(self, event):
        self.transpor()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.transpor()
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
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def horizontal_move_exists(self):
        for row in range(4):
            for col in range(3):
                if self.matriz[row][col] == self.matriz[row][col + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for row in range(3):
            for col in range(4):
                if self.matriz[row][col] == self.matriz[row + 1][col]:
                    return True
        return False

    def fim_de_jogo(self):
        if any(2048 in row for row in self.matriz):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="VITÓRIA!",
                bg=cores.FUNDO_VENCEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
        elif not any(0 in row for row in self.matriz) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="DERROTA!",
                bg=cores.FUNDO_PERDEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
            
Jogo()