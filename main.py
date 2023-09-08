import random

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

def esquerda():
    empilhar()
    combinar()
    empilhar()
    add_nova_peca()
    mostra_a_matriz()

def direita():
    reverter()
    empilhar()
    combinar()
    empilhar()
    reverter()
    add_nova_peca()
    mostra_a_matriz()

def cima():
    transpor()
    empilhar()
    combinar()
    empilhar()
    transpor()
    add_nova_peca()
    mostra_a_matriz()



def baixo():
    transpor()
    reverter()
    empilhar()
    combinar()
    empilhar()
    reverter()
    transpor()
    add_nova_peca()
    mostra_a_matriz()

start_game()

parar = True
while parar:
    escolha = input("> ")
    if escolha == 'a':
        esquerda()
    elif escolha == 'd':
        direita()
    elif escolha == 'w':
        cima()
    elif escolha == 's':
        baixo()
    elif escolha == 'sair':
        parar = False
    


