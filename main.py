import random
import os
if os.name == 'nt':
    import msvcrt

score = 0

def start_game():
    global matriz
    matriz = [[0] * 4 for _ in range(4)]

    row = random.randint(0, 3)
    col = random.randint(0, 3)
    matriz[row][col] = 2

    while(matriz[row][col] != 0):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
    matriz[row][col] = 2

    print("""
    BOTÕES: 
    ↓ ← → ↑ - Teclas de Direção
    q - Finaliza o Jogo
    """)

    mostra_a_matriz()

def empilhar():
    global matriz
    nova_matriz = [[0] * 4 for _ in range(4)]
    for row in range(4):
        posicao_preenchida = 0
        for col in range(4):
            if matriz[row][col] != 0:
                nova_matriz[row][posicao_preenchida] = matriz[row][col]
                posicao_preenchida += 1
    matriz = nova_matriz

def combinar():
    global matriz
    global score
    for row in range(4):
        for col in range(3):
            if matriz[row][col] != 0 and matriz[row][col] == matriz[row][col + 1]:
                matriz[row][col] *= 2
                matriz[row][col + 1] = 0
                score += matriz[row][col]

def reverter():
    global matriz
    nova_matriz = []
    for row in range(4):
        nova_matriz.append([])
        for col in range(4):
            nova_matriz[row].append(matriz[row][3 - col])
    matriz = nova_matriz

def transpor():
    global matriz
    nova_matriz = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for col in range(4):
            nova_matriz[row][col] = matriz[col][row]
    matriz = nova_matriz

def add_nova_peca():
    global matriz
    if any(0 in row for row in matriz):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(matriz[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        if random.random() < 0.9:
            matriz[row][col] = 2
        else:
            matriz[row][col] = 4

def mostra_a_matriz():
    global matriz
    print()
    print(f"Score: {score}")
    for row in range(4):
        print(matriz[row])

def horizontal_move_exists():
    global matriz
    for row in range(4):
        for col in range(3):
            if matriz[row][col] == matriz[row][col + 1]:
                return True
    return False

def vertical_move_exists():
    global matriz
    for row in range(3):
        for col in range(4):
            if matriz[row][col] == matriz[row + 1][col]:
                return True
    return False

def fim_de_jogo():
    global matriz
    global parar
    if any(2048 in row for row in matriz):
        print("VITÓRIA !!")
        parar = False
    elif not any(0 in row for row in matriz) and not horizontal_move_exists() and not vertical_move_exists():
        print("VOCÊ PERDEU !!")
        parar = False

def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        # Limpa o terminal em sistemas não-Windows (Linux, macOS, etc.)
        os.system('clear')

def esquerda():
    limpar_terminal()
    empilhar()
    combinar()
    empilhar()
    add_nova_peca()
    mostra_a_matriz()
    fim_de_jogo()

def direita():
    limpar_terminal()
    reverter()
    empilhar()
    combinar()
    empilhar()
    reverter()
    add_nova_peca()
    mostra_a_matriz()
    fim_de_jogo()

def cima():
    limpar_terminal()
    transpor()
    empilhar()
    combinar()
    empilhar()
    transpor()
    add_nova_peca()
    mostra_a_matriz()
    fim_de_jogo()

def baixo():
    limpar_terminal()
    transpor()
    reverter()
    empilhar()
    combinar()
    empilhar()
    reverter()
    transpor()
    add_nova_peca()
    mostra_a_matriz()
    fim_de_jogo()

# Comandos em sistemas não-Windows (Linux, macOS, etc.)
def linux_mac():
    parar = True
    while parar:
        print("\n[a] - Esquerda; [d] - Direita; [s] - Baixo; [w] - Cima \n[sair] - Finalizar Jogo")
        tecla = input(">>> ")
        if tecla == 's':
            baixo()
        elif tecla == 'w':
            cima()
        elif tecla == 'a':
            esquerda()
        elif tecla == 'd':
            direita()
        elif tecla == "sair":
            parar = False
        else:
            print("\033[1;30;31mTecla Inválida\033[0m")

# Comandos para Windows
def windows():
    key = msvcrt.getch()
    while parar:
        if key == b'q': 
            parar = False  # Sair do loop se 'q' for pressionado
        elif key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                cima()
            elif key == b'P':
                baixo()
            elif key == b'M':
                direita()
            elif key == b'K':
                esquerda()


start_game()

if os.name == 'nt':
    windows()
else:
    linux_mac()
