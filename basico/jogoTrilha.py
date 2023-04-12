# -*- coding: utf-8 -*-

import socket

#______JOGO---TRILHA_____
#AUTORES: ALLISON PLATTYNIR, ANGELICA, DIEGO DE LIMA E MATHEUS.
#DISCIPLINA: Progamacao pra Redes. PROF: Joao.
#Descricao
#O jogo de Trilha tem dois participantes, que usam um tabuleiro para jogar.
#Jogadores - 2
#Peças - 18 peças sendo 9 brancas e 9 pretas.(x e o)
#Tabuleiro - tabuleiro com 24 casa interligados horizontalmente e verticalmente.
#Objetivo - Deixar o adversário com 2 peças no tabuleiro ou deixá-lo sem movimentos.


#Tabuleiro e definiçoes_____________________________________________________________
trilha = """JOGO TRILHA                                        POSICOES
( )--------------------( )--------------------( )  #(1)--------------------(2)--------------------(3)
 |                      |                      |   # |                      |                      |
 |      ( )------------( )------------( )      |   # |      (4)------------(5)------------(6)      |
 |       |              |              |       |   # |       |              |              |       |
 |       |      ( )----( )----( )      |       |   # |       |      (7)----(8)----(9)      |       |
 |       |       |             |       |       |   # |       |       |             |       |       |
( )-----( )-----( )           ( )-----( )-----( )  #(10)----(11)----(12)          (13)----(14)----(15)
 |       |       |             |       |       |   # |       |       |             |       |       |
 |       |      ( )----( )----( )      |       |   # |       |      (16)---(17)---(18)     |       |
 |       |              |              |       |   # |       |              |              |       |
 |      ( )------------( )------------( )      |   # |      (19)-----------(20)-----------(21)     |
 |                      |                      |   # |                      |                      |
( )--------------------( )--------------------( )  #(22)-------------------(23)-------------------(24)

"""
# Uma lista de posições (linha e coluna) para cada posição válida do jogo
# Um elemento extra foi adicionado para facilitar a manipulação
# dos índices e para que estes tenham o mesmo valor da posição
#(1)--------------------(2)--------------------(3)
# |                      |                      |
# |      (4)------------(5)------------(6)      |
# |       |              |              |       |
# |       |      (7)----(8)----(9)      |       |
# |       |       |             |       |       |
#(10)----(11)----(12)          (13)----(14)----(15)
# |       |       |             |       |       |
# |       |      (16)---(17)---(18)     |       |
# |       |              |              |       |
# |      (19)-----------(20)-----------(21)     |
# |                      |                      |
#(22)-------------------(23)-------------------(24)

posicoes = [
       None,  # Elemento adicionado para facilitar índices
       (1, 1), # 1
       (1, 24), # 2
       (1, 47), # 3
       (3, 9), # 4
       (3, 24), # 5
       (3, 39), # 6
       (5, 17), # 7
       (5, 24), # 8
       (5, 31), # 9
       (7,1),# 10
       (7,9),# 11
       (7,17),# 12
       (7,31),# 13
       (7,39),# 14
       (7,47),# 15
       (9,17),# 16
       (9,24),# 17
       (9,31),# 18
       (11,9),# 19
       (11,24),# 20
       (11,39),# 21
       (13,1),# 22
       (13,24),# 23
       (13,47),# 24
    ]

# Posições que levam ao ganho do jogo
# Jogadas fazendo uma linha ou coluna
# Os números representam as posições ganhadoras
ganho = [
    
          [ 1, 2, 3], # Linhas
          [ 4, 5, 6],
          [ 7, 8, 9], 
          [ 10, 11, 12],
          [ 13, 14, 15],
          [ 16, 17, 18],
          [ 19, 20, 21],
          [ 22, 23, 24],
          [ 1, 10, 22], # Colunas
          [ 4, 11, 19],
          [ 7, 12, 16],
          [ 2, 5, 8],
          [ 17, 20, 23],
          [ 9, 13, 18],
          [ 6, 14, 21],
          [ 3, 15, 24],
        ]

# Constroi o tabuleiro a partir da string
# Gerando uma lista de listas que pode ser modificada
tabuleiro = []
for linha in trilha.splitlines():
    tabuleiro.append(list(linha))

# Verifica se a peca informada faz parte de um moinho
def faz_parte_trilha( peca, jogador ):
    for p in ganho:
        jogou_nessa_linha = False
        e_moinho = True
        for x in p:
            if x == peca:
                jogou_nessa_linha = True
            if tabuleiro[posicoes[x][0]][posicoes[x][1]] != jogador:
                e_moinho = False
                break
        if jogou_nessa_linha and e_moinho:
            return True
    
    return False

# verifica se o jogador tem peca soltar para mover ou se so tem peca dentro de trila
def tem_peca_solta(jogador):
    for x in range(1, 24):
        if tabuleiro[posicoes[x][0]][posicoes[x][1]] == jogador and not faz_parte_trilha(x, jogador):
            return True
    
    return False

# conta quantas pecas o jogador tem no tabuleiro
def conta_pecas(jogador):
    contador = 0
    for x in range(1, 24):
        if tabuleiro[posicoes[x][0]][posicoes[x][1]] == jogador:
            contador += 1
    return contador

#_________________________Conectando aos clientes:__________________________________________________________
HOST = ''              # Endereco IP do Servidor
PORT_X = 5000         
PORT_O = 5001

tcp_x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig_x = (HOST, PORT_X)
tcp_x.bind(orig_x)
tcp_x.listen(1)

print("Aguardando o Jogador X")
con_x, cliente_x = tcp_x.accept()

tcp_o = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig_o = (HOST, PORT_O)
tcp_o.bind(orig_o)
tcp_o.listen(1)

print("Aguardando o Jogador O")
con_o, cliente_o = tcp_o.accept()

def valida_input_int(s):
    if len(s) <= 0:
        return False
    try: 
        int(s)
        return True
    except ValueError:
        return False

def recebe_input(mensagem, jogador):
    socket_print(mensagem + "\r", jogador)
    if jogador == "X":
        resposta = con_x.recv(5120).decode("utf-8")
    elif jogador == "O":
        resposta = con_o.recv(5120).decode("utf-8")
    valido = valida_input_int(resposta)
    while not valido:
        socket_print(mensagem + "\r", jogador)
        if jogador == "X":
            resposta = con_x.recv(5120).decode("utf-8")
        elif jogador == "O":
            resposta = con_o.recv(5120).decode("utf-8")
        valido = valida_input_int(resposta)
    
    return resposta

def socket_print(mensagem, jogador):
    mensagem
    if jogador == "X":
        con_x.send(mensagem.encode('utf-8'))
    elif jogador == "O":
        con_o.send(mensagem.encode('utf-8'))
    else:
        con_x.send(mensagem.encode('utf-8'))
        con_o.send(mensagem.encode('utf-8'))

#_________________________Colocando as peças:__________________________________________________________

jogador = "X" # Começa jogando com X
adversario = "O"
jogando = True
jogadas = 0 # Contador de jogadas - usado para saber se foi Trilha
while jogando:
    print("Jogada: %d" % jogadas)
    output = ""
    for t in tabuleiro:  # Imprime o tabuleiro
        linha = "".join(t)
        output += linha+"\n"
        print(linha)
        
    socket_print(output, "todos")
    
    if not jogando: # Termina após imprimir o último tabuleiro
        break
        
    if jogadas >= 18: # Se 18 jogadas foram feitas, todas as posições já foram preenchidas
        socket_print("Todas as pecas colocadas.", "todos")
        
    if jogadas < 18:
        jogada = int(recebe_input("Digite a posicao a jogar 1-24 (jogador %s):" % jogador, jogador))
        if jogada<1 or jogada>24:
            socket_print("Posicao invalida", jogador)
            continue
    elif conta_pecas(jogador) <= 2:
        socket_print("O jogador %s venceu!" % adversario, "todos")
        jogando = False
        break
    elif conta_pecas(adversario) <= 2:
        socket_print("O jogador %s venceu!" % jogador, "todos")
        jogando = False
        break
    else:
        peca = int(recebe_input("Digite a peca que deseja mover 1-24 (jogador %s):" % jogador, jogador))
        while peca<1 or peca>24 or tabuleiro[posicoes[peca][0]][posicoes[peca][1]] != jogador:
            socket_print("Peca invalida", jogador)
            peca = int(recebe_input("Digite a peca que deseja mover 1-24 (jogador %s):" % jogador, jogador))
        
        jogada = int(recebe_input("Digite a posicao para mover a peca 1-24 (jogador %s):" % jogador, jogador))
        while jogada<1 or jogada>24 or tabuleiro[posicoes[jogada][0]][posicoes[jogada][1]] != " ":
            socket_print("Posicao invalida", jogador)
            jogada = int(recebe_input("Digite a posicao para mover a peca 1-24 (jogador %s):" % jogador, jogador))
            
        tabuleiro[posicoes[peca][0]][posicoes[peca][1]] = " "
            
    # Verifica se a posição está livre________________________________________________________
    if tabuleiro[posicoes[jogada][0]][posicoes[jogada][1]] != " ":
        socket_print("Posicao ocupada.", jogador);
        continue
    tabuleiro[posicoes[jogada][0]][posicoes[jogada][1]] = jogador
    # Trilha ou Moinho______________
    if faz_parte_trilha(jogada, jogador): # Se o for terminar sem break, todas as posicoes de p pertencem ao mesmo jogador
        socket_print("O jogador %s formou uma Trilha: "%(jogador), "todos")
        socket_print("= Remover uma peca do adversario! =", jogador)
        jogada = int(recebe_input("Digite a posicao da peca adversaria a remover 1-24 (jogador %s):" % jogador, jogador))
        while jogada<1 or jogada>24 or tabuleiro[posicoes[jogada][0]][posicoes[jogada][1]] != adversario or (faz_parte_trilha(jogada, adversario) and tem_peca_solta(adversario)):
            socket_print("Posicao invalida", jogador)
            jogada = int(recebe_input("Digite a posicao da peca adversaria a remover 1-24 (jogador %s):" % jogador, jogador))

        tabuleiro[posicoes[jogada][0]][posicoes[jogada][1]] = " "

        #jogando = False
        #break
    
    reserva = jogador
    jogador = adversario # Alterna jogador
    adversario = reserva
    jogadas +=1 # Contador de jogadas

    
tcp.close()

# Sobre a conversão de coordenadas:
# tabuleiro[posições[x][0]][posições[x][1]]


# O Jogo
# O jogo consiste em tres partes principais:______________
# Colocando as peças: Esta é a fase inicial do jogo onde cada jogador coloca um peça de cada vez alternando entre jogadores, caso um dos jogadores forme uma linha horizontal ou vertical com três peças (um moinho), ele terá o direito de remover uma peça de seu adversário do tabuleiro.
# Movendo as peças: Esta fase se inicia quando ambos os jogadores colocarem suas nove peças em jogo. Consiste em mover suas peças ao longo de uma das linhas do tabuleiro para uma outra casa adjacente. Caso um dos jogadores tenha somente 3 peças em jogo, ele pode "voar" com suas peças, podendo mover para qualquer casa que não esteja ocupada por uma peça do adversário.
# Removendo peças adversárias: Em qualquer uma das fases acima quando um jogador forma uma linha horizontal ou vertical com 3 peças ele fará um "moinho", isso lhe dá o direito de remover uma peça de seu adversário, contudo você não poderá remover uma peça do seu adversário que faz parte de um moinho dele, a não ser que não exista outra peça para remover.

# Estratégia_______________________________________
# No começo do jogo, é muito importante colocar as peças nos lugares mais versáteis para tentar formar imediatamente moinhos e não cometer o erro de concentrar as peças próprias em uma área do tabuleiro.
# Uma posição ideal, que geralmente resulta em uma vitória, é ser capaz de colocar uma peça que possa se movimentar entre dois moinhos diferentes00

# Fim da Partida___________________________________
# O jogo termina quando 3 situações são alcançadas:
# Se um jogador reduzir as peças de seu adversário para 2.
# Se um jogador deixar seu adversário sem nenhuma jogada válida. Caso seu adversário tenha somente 3 peças em jogo, ele não poderá ser "trancado".
# Se ambos jogadores estiverem com 3 peças em jogo e, a partir deste momento, se em 10 jogadas não houver vencedor, o jogo terminará e será declarado um empate.



