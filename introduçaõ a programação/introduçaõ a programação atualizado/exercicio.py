"""
Pacman

Este jogo está parcialmente implementado.
Seu objetivo é compreender o funcionamento do código
e completar ou melhorar os trechos indicados com TODO,
para que fique funcionalmente semelhante ao jogo
presente no pacote freegames.

Depois, você deverá resolver os desafios propostos abaixo.

Desafios:
1. Alterar o tabuleiro.
2. Remover a comida após ser coletada
3. Alterar a quantidade de fantasmas.
4. Alterar a posição inicial do Pacman.
5. Alterar a velocidade dos fantasmas.
6. Identificar jogador em cada rodada. Qual o nome do jogador que vai iniciar um jogo?
7. Tornar o jogo para dois jogadores.
8. Armazenar jogador e suas pontuações em arquivo. Ao final do jogo, armazenar em arquivo
o nome do jogador que jogou e sua respectiva pontuação na rodada.
A pontuação a ser gravada é a quantidade de comida que o Pacman comeu na rodada.
9. Listar jogadores e suas pontuações. Exibir no terminal uma lista de todos os jogadores
que jogaram o jogo com suas respectivas pontuações.
"""

from random import choice
import turtle
from freegames import floor, vector
jogador_atual = input("digite o seu nome:")
jogadores = []
for i in range(2):
  nome = input(f"Digite o nome do jogador {i+1}: ")
  jogadores.append(nome)

jogador_atual = jogadores[0]
ARQUIVO_PONTOS="pontuacoes.txt"

estado = {'pontuacao': 0}
caminho = turtle.Turtle(visible=False)
escritor = turtle.Turtle(visible=False)
direcao = vector(10, 0)
pacman = vector( 20, -40)

fantasmas = [
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
    [vector(100, 160), vector(-10 , 0)],
    [vector(100, 160), vector(-10 , 0)],
]


# Mapa do jogo (0 = parede, 1 = comida, 2 = vazio)
tiles = [

0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,
0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,
0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,
0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,
0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,
0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,
0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,
0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,
0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,
0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,
0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,
0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,
0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,
0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,
0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

def quadrado(x, y):
    """Desenha um quadrado do tabuleiro."""
    caminho.up()
    caminho.goto(x, y)
    caminho.down()
    caminho.begin_fill()
    for _ in range(4):
        caminho.forward(20)
        caminho.left(90)
    caminho.end_fill()


def indice(ponto):
    """Converte posição (x, y) em índice do mapa."""
    x = (floor(ponto.x, 20) + 200) / 20
    y = (180 - floor(ponto.y, 20)) / 20
    return int(x + y * 20)

def salvar_pontuacao(nome, pontos):
    with open(ARQUIVO_PONTOS, "a") as arquivo:
        arquivo.write(f"{nome} - {pontos}\n")

def valido(ponto):
    """Verifica se o movimento é permitido."""
    if tiles[indice(ponto)] == 0:
        return False
    if tiles[indice(ponto + 19)] == 0:
        return False
    return ponto.x % 20 == 0 or ponto.y % 20 == 0


def mundo():
    """Desenha o tabuleiro e as comidas."""
    turtle.bgcolor('black')
    caminho.color('purple')

    for i, tile in enumerate(tiles):
        if tile > 0:
            x = (i % 20) * 20 - 200
            y = 180 - (i // 20) * 20
            quadrado(x, y)

            if tile == 1:
                caminho.up()
                caminho.goto(x + 10, y + 10)
                caminho.dot(2, 'white')


def mover():
    """Laço principal do jogo."""
    escritor.undo()
    escritor.write(estado['pontuacao'])
    turtle.clear()
    
    if valido(pacman + direcao):
        pacman.move(direcao)

    idx = indice(pacman)

    if tiles[idx] == 1:
        tiles[idx] = 2
        estado['pontuacao'] += 1
    

        # TODO desenhar quadrado vazio no lugar da comida
        
        x=(idx % 20) * 20-200
        y= 180 - (idx // 20) * 20
        caminho.color("purple")
        quadrado(x ,y)
        caminho.color("blue")
    
    turtle.up()
    turtle.goto(pacman.x + 10, pacman.y + 10)
    turtle.dot(20, 'yellow')

    for ponto, curso in fantasmas:
        if valido(ponto + curso):
            ponto.move(curso)
        else:
            opções = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
                vector(0, 10),
            ]
            escolhido = choice(opções)
            curso.x = escolhido.x
            curso.y = escolhido.y

        turtle.up()
        turtle.goto(ponto.x + 10, ponto.y + 10)
        turtle.dot(20, 'red')

    turtle.update()

    for ponto, _ in fantasmas:
        if abs(pacman - ponto) < 20:
            return

    turtle.ontimer(mover, 100)

def listar_pontuacoes():
    print("\n===== PONTUAÇÕES REGISTRADAS =====")

    try:
        with open("pontuacoes.txt", "r") as arquivo:
            for linha in arquivo:
                print(linha.strip())
    except FileNotFoundError:
        print("Nenhuma pontuação encontrada.")

def mudar(x, y):
    """Altera a direção do Pacman."""
    if valido(pacman + vector(x, y)):
        direcao.x = x
        direcao.y = y
salvar_pontuacao(jogador_atual, estado['pontuacao'])


# Configuração gráfica
turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)

# TODO o escritor deve caminhar sem deixar rastro
escritor.penup()
escritor.color('white')
escritor.goto(160, 160)
escritor.write(estado['pontuacao'])

turtle.listen()
turtle.onkey(lambda: mudar(5, 0), 'Right')
turtle.onkey(lambda: mudar(-5, 0), 'Left')
turtle.onkey(lambda: mudar(0, 5), 'Up')
turtle.onkey(lambda: mudar(0, -5), 'Down')
listar_pontuacoes()
mundo()
mover()
turtle.mainloop()