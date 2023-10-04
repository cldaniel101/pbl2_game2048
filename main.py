"""
Autor: Cláudio Daniel Figueredo Peruna
Componente Curricular: EXA 854 - MI - Algoritmos
ConcluÍdo em: 03/10/2023
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
"""

import tkinter as tk
import random
import cores

class Jogo(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)  # Construtor do Tkinter para inicializar a janela
        self.grid()  # Organiza os widgets dentro da janela
        self.master.title('2048') 

        # Aqui, está sendo criado um quadro principal dentro da janela e colocando na grade principal
        self.grade_principal = tk.Frame(
            self, bg=cores.COR_GRADE, bd=3, width=400, height=400) 
        self.grade_principal.grid(pady=(80, 0)) 

        # Cria a interface gráfica e inicia o jogo
        self.criar_Interface()
        self.start_game()

        # Controla o movimento das peças 
        self.master.bind("<Left>", self.esquerda)
        self.master.bind("<Right>", self.direita)
        self.master.bind("<Up>", self.cima)
        self.master.bind("<Down>", self.baixo)

        # Mantém o jogo aberto até que a janela seja fechada
        self.mainloop()

    def criar_Interface(self):
        # Inicializa a lista de células vazias
        self.celulas = []

        # Loop para criar uma matriz 4x4 de células
        for i in range(4):
            linha = []  # Inicializa uma lista para representar uma linha na grade
            for j in range(4):
                # Cria um quadrado para representar uma célula vazia
                quadrado_celula = tk.Frame(
                    self.grade_principal,  # Onde a célula será colocada
                    bg=cores.COR_CELULA_VAZIA,  # Cor de fundo da célula vazia
                    width=100,  # Largura da célula
                    height=100  # Altura da célula
                )
                quadrado_celula.grid(row=i, column=j, padx=5, pady=5)  # Coloca a célula na grade
                numero_da_celula = tk.Label(self.grade_principal, bg=cores.COR_CELULA_VAZIA)  # Cria um rótulo para o número na célula
                numero_da_celula.grid(row=i, column=j)  # Coloca o rótulo na grade
                celula = {"frame": quadrado_celula, "number": numero_da_celula}  # Representa a célula como um dicionário
                linha.append(celula)  # Adiciona a célula à linha
            self.celulas.append(linha)  # Adiciona a linha à lista de células

        # Cria um quadro para exibir a pontuação (score)
        frame_do_score = tk.Frame(self)
        frame_do_score.place(relx=0.5, y=40, anchor="center")

        # Adiciona um rótulo para indicar "Score"
        tk.Label(
            frame_do_score,
            text="Score",
            font=cores.FONTE_ROTULO_PONTUACAO
        ).grid(row=0)

        # Cria um rótulo para exibir a pontuação atual
        self.legenda_score = tk.Label(frame_do_score, text="0", font=cores.FONTE_PONTUACAO)
        self.legenda_score.grid(row=1)

    def atualizar_Interface(self):
        for i in range(4):
            for j in range(4):
                valor_da_celula = self.matriz[i][j]

                if valor_da_celula == 0:
                    # Configura a cor de fundo da célula como vazia (background)
                    self.celulas[i][j]["frame"].configure(bg=cores.COR_CELULA_VAZIA)
                    # Remove o texto da célula
                    self.celulas[i][j]["number"].configure(bg=cores.COR_CELULA_VAZIA, text="")
                else:
                    # Configura a cor de fundo da célula com base no valor da célula
                    self.celulas[i][j]["frame"].configure(bg=cores.CORES_CELULA[valor_da_celula])
                    # Configura a cor do texto, a fonte e o texto da célula com base no valor da célula
                    self.celulas[i][j]["number"].configure(
                        bg=cores.CORES_CELULA[valor_da_celula],
                        fg=cores.CORES_NUMERO_CELULA[valor_da_celula],
                        font=cores.FONTE_NUMERO_CELULA[valor_da_celula],
                        text=str(valor_da_celula))
        
        # Atualiza o rótulo da pontuação (score) com a pontuação atual
        self.legenda_score.configure(text=self.score)
        # Atualiza a interface gráfica
        self.update_idletasks()


    def start_game(self):
        self.fim = False  # Variavel apenas para verificar se o jogo acabou ou não

        # Inicializa a matriz do jogo como uma matriz 4x4 preenchida com zeros
        self.matriz = [[0] * 4 for _ in range(4)]

        # Gera aleatoriamente uma posição inicial para um novo número (2)
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matriz[row][col] = 2
        # Atualiza a cor de fundo e o texto da célula correspondente ao novo número
        self.celulas[row][col]["frame"].configure(bg=cores.CORES_CELULA[2])
        self.celulas[row][col]["number"].configure(
            bg=cores.CORES_CELULA[2],
            fg=cores.CORES_NUMERO_CELULA[2],
            font=cores.FONTE_NUMERO_CELULA[2],
            text="2")

        # Continua gerando aleatoriamente uma posição até encontrar uma célula vazia (com valor 0)
        while(self.matriz[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        # Insere um novo número (2) na célula encontrada
        self.matriz[row][col] = 2
        # Atualiza a cor de fundo e o texto da célula correspondente ao novo número
        self.celulas[row][col]["frame"].configure(bg=cores.CORES_CELULA[2])
        self.celulas[row][col]["number"].configure(
            bg=cores.CORES_CELULA[2],
            fg=cores.CORES_NUMERO_CELULA[2],
            font=cores.FONTE_NUMERO_CELULA[2],
            text="2")

        # Inicializa a pontuação (score) como zero e o número de jogadas como zero
        self.score = 0
        self.jogadas = 0


    def empilhar(self):
        # Cria uma nova matriz 4x4 preenchida com zeros
        nova_matriz = [[0] * 4 for _ in range(4)]

        # Itera pelas linhas da matriz atual
        for row in range(4):
            posicao_preenchida = 0  # Inicializa uma variável para rastrear a posição preenchida na nova linha
            # Itera pelas colunas da matriz atual
            for col in range(4):
                # Verifica se o valor na célula atual não é zero (ou seja, não é uma célula vazia)
                if self.matriz[row][col] != 0:
                    # Copia o valor da célula atual para a próxima posição preenchida na nova matriz
                    nova_matriz[row][posicao_preenchida] = self.matriz[row][col]
                    posicao_preenchida += 1  # Incrementa a posição preenchida na nova linha

        # Atualiza a matriz do jogo com a nova matriz após o empilhamento
        self.matriz = nova_matriz


    def combinar(self):
        for row in range(4):
            # Itera pelas colunas, exceto a última
            for col in range(3):
                # Verifica se o valor na célula atual não é zero e se é igual ao próximo valor na mesma linha
                if self.matriz[row][col] != 0 and self.matriz[row][col] == self.matriz[row][col + 1]:
                    # Se forem iguais, dobra o valor da célula atual
                    self.matriz[row][col] *= 2
                    # Define o valor da próxima célula como zero (pois foi combinada com a atual)
                    self.matriz[row][col + 1] = 0
                    # Atualiza a pontuação (score) adicionando o valor dobrado à pontuação atual
                    self.score += self.matriz[row][col]


    def reverter(self):
        # Cria uma nova matriz vazia para armazenar a matriz revertida
        nova_matriz = []

        for row in range(4):
            nova_matriz.append([])  # Adiciona uma nova lista vazia para representar uma linha na nova matriz
            for col in range(4):
                # Copia os valores da matriz original na ordem reversa para a nova matriz
                nova_matriz[row].append(self.matriz[row][3 - col])

        self.matriz = nova_matriz


    def transpor(self):
        nova_matriz = [[0] * 4 for _ in range(4)]

        for row in range(4):
            for col in range(4):
                # Copia os valores da matriz original para a nova matriz, trocando as posições de linha e coluna
                nova_matriz[row][col] = self.matriz[col][row]

        self.matriz = nova_matriz


    def add_nova_peca(self):
        # Verifica se ainda existem células vazias na matriz
        if any(0 in row for row in self.matriz):
            # Escolhe aleatoriamente uma posição vazia na matriz
            row = random.randint(0, 3)
            col = random.randint(0, 3)

            while(self.matriz[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)

            # Gera aleatoriamente um número 2 com probabilidade de 90% e 4 com probabilidade de 10%
            if random.random() < 0.9:
                self.matriz[row][col] = 2
            else:
                self.matriz[row][col] = 4



    # MOVIMENTOS
    def esquerda(self, event):
        self.empilhar()
        self.combinar()
        self.empilhar()
        if not self.fim:
            self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()

    def direita(self, event):
        self.reverter()
        self.empilhar()
        self.combinar()
        self.empilhar()
        self.reverter()
        if not self.fim:
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
        if not self.fim:
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
        if not self.fim:
            self.jogadas += 1
        self.add_nova_peca()
        self.atualizar_Interface()
        self.fim_de_jogo()


    def existe_mov_horizontal(self):
        for row in range(4):
            for col in range(3):
                # Verifica se o valor na célula atual é igual ao valor na próxima célula na mesma linha
                if self.matriz[row][col] == self.matriz[row][col + 1]:
                    return True  # Se houver uma combinação possível, retorna True
        return False  # Se não houver combinações possíveis, retorna False

    # Segue a mesma lógica da verificação horizontal.
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
            font=cores.FONTE_PONTUACAO_FINAL).pack()
        
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
    

    def reiniciar(self):
        self.master.destroy() # Fecha a antiga janela
        Jogo() # Abre um novo jogo

    def botao_reiniciar(self):
        frame_reiniciar = tk.Frame(self.grade_principal, borderwidth=2)
        frame_reiniciar.place(relx=0.5, rely=0.85, anchor="center")
        tk.Button(
            frame_reiniciar, 
            text="Reiniciar", 
            bg="#5E12E6",
            fg=cores.COR_FONTE_FIM_DE_JOGO,
            font=cores.FONTE_JOGADAS_RECORDE,
            command=self.reiniciar
            ).pack()
        
        
    def ler_recorde(self):
        try:
            with open("recorde.txt", "r") as arquivo: 
                # Abre o arquivo chamado recorde e lê o que tem dentro
                recorde = int(arquivo.read())
            return recorde
        except FileNotFoundError:
            # Se não encontrar o arquivo, cria um novo com o valor 0 dentro
            recorde = 0
            with open("recorde.txt", "w") as arquivo:
                arquivo.write(str(recorde))
            return recorde

        
    def verifica_recorde(self):
        recorde = self.ler_recorde()  # Lê o recorde atual

        if self.score > recorde:
            # Se a pontuação atual for maior que o recorde anterior, atualiza o recorde
            with open("recorde.txt", "w") as arquivo:
                arquivo.write(str(self.score))

    # TESTES (Leia o relatório)

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

    def fim_de_jogo(self):
        # Verifica se o jogador alcançou 2048
        if any(2048 in row for row in self.matriz):
            # Cria um quadro para exibir a mensagem de vitória
            frame_fim_de_jogo = tk.Frame(self.grade_principal, borderwidth=2)
            frame_fim_de_jogo.place(relx=0.5, rely=0.20, anchor="center")
            tk.Label(
                frame_fim_de_jogo,
                text="VITÓRIA!",
                bg=cores.FUNDO_VENCEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
            self.fim = True
            self.verifica_recorde()  
            self.mostra_jogadas_e_recorde() 
            self.botao_reiniciar() 
        # Verifica se não há células vazias e nenhum movimento horizontal ou vertical é possível
        elif not any(0 in row for row in self.matriz) \
                and not self.existe_mov_horizontal() \
                and not self.existe_mov_vertical():
            # Cria um quadro para exibir a mensagem de derrota
            frame_fim_de_jogo = tk.Frame(self.grade_principal, borderwidth=2)
            frame_fim_de_jogo.place(relx=0.5, rely=0.20, anchor="center")
            tk.Label(
                frame_fim_de_jogo,
                text="DERROTA!",
                bg=cores.FUNDO_PERDEDOR,
                fg=cores.COR_FONTE_FIM_DE_JOGO,
                font=cores.FONTE_FIM_DE_JOGO).pack()
            self.fim = True
            self.verifica_recorde()
            self.mostra_jogadas_e_recorde()
            self.botao_reiniciar()


Jogo()
