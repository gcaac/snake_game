#Jogo da cobrinha (base pela kenzie, aprimorações por mim)#

import sys       #para poder fechar a janela depois#
import pygame    #ativando a biblioteca gráfica para os joguinhos#
import random    #ativando o gerador aleatório#
import time      #para dar pausas no jogo#


#gerando o tipo de fonte dos textos printados#
pygame.font.init()
font = pygame.font.SysFont('comicsansms',30)
font2 = pygame.font.SysFont('comicsansms',20)
font3 = pygame.font.SysFont('comicsansms',40)

dimensoes = (600, 600) #variável de tupla que representará o tamanho do display(tela)#

#gerando variáveis com triplas de cores#
azul = (50, 100, 213)
rosa = (245, 98, 206)
verde = (0, 255, 0)
roxo = (84, 49, 120)
branco = (250, 250, 250)
vermelho = (214, 15, 15)

#Gerando a tela#
tela = pygame.display.set_mode((dimensoes))                           #gerando a tela base#
pygame.display.set_caption('Snake Game    (Press Esc to close)')      #nomezinho que aparece em cima#
tela.fill(azul)


#menu inicial#
def menu():
    while True:
        for event in pygame.event.get():  # para o pygame identificar as teclas sendo pegas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    main()
        tela.fill(roxo)
        game_title = font3.render('SNAKE GAME', True, rosa)
        tela.blit(game_title, (160, 30))
        mensagem_menu1 = font2.render('Pressione: Enter (para iniciar)', True, verde)
        tela.blit(mensagem_menu1, (160, 300))
        mensagem_menu2 = font2.render('Esc (para sair)', True, verde)
        tela.blit(mensagem_menu2, (261, 330))
        author = font2.render('Giulia Carvalho - 2021', True, branco)
        tela.blit(author, (390, 560))
        pygame.display.update()


#Contém as funções gerais do funcionamento do jogo!!#
def main():

    x = 300                    # (x,y) = valores centrais #
    y = 300
    d = 20                     # d = dimensão do quadrado que é a cobra #
    score = 0                  # score = pontos #
    lista_cobra = [[x, y]]     # a lista é a cobrinha em si #
    dx = 0                     # dx e dy = 'direções' da cobrinha #
    dy = 0
    dir = ''
    x_comida = round(random.randrange(0, 600 - d) / 20) * 20
    y_comida = round(random.randrange(0, 600 - d) / 20) * 20

    clock = pygame.time.Clock()  # define a velocidade no qual a tela se atualiza (quase um fps)


    #cuida do game over do jogo#
    def game_over(score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            tela.fill((224, 121, 121))
            mensagem_gameover = font3.render('Você perdeu...    :(', True, vermelho)
            tela.blit(mensagem_gameover, (140, 100))
            score_gameover = font2.render(f'Você fez: {score} pontos!', True, branco)
            tela.blit(score_gameover, (190, 330))
            aviso = font2.render('Redirecionando para o menu...', True, branco)
            tela.blit(aviso, (300, 560))
            pygame.display.update()
            time.sleep(3)
            menu()


    #Cria a cobra visualmente#
    def desenha_cobra(lista_cobra):
        tela.fill(azul)
        for unidade in lista_cobra:
            pygame.draw.rect(tela, rosa, [unidade[0], unidade[1], d, d])  # tela em que vai aparecer, cor dele e posição

    #cuida do movimento da cobra#
    def mover_cobra(dx, dy, lista_cobra, dir):
        for event in pygame.event.get():  # para o pygame identificar as teclas sendo pegas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dir != 'direita':
                    dx = -d
                    dy = 0
                    dir = 'esquerda'
                elif event.key == pygame.K_RIGHT and dir != 'esquerda':
                    dx = d
                    dy = 0
                    dir = 'direita'
                elif event.key == pygame.K_UP and dir != 'baixo':
                    dx = 0
                    dy = -d
                    dir = 'cima'
                elif event.key == pygame.K_DOWN and dir != 'cima':
                    dx = 0
                    dy = d
                    dir = 'baixo'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # atualizando os valores novos da lista
        x_novo = lista_cobra[-1][0] + dx
        y_novo = lista_cobra[-1][1] + dy

        #fecha o jogo caso a cobrinha bata na parede!#
        if x_novo < 0 or x_novo > 600:
            game_over(score)
        elif y_novo < 0 or y_novo > 600:
            game_over(score)

        #fecha o jogo caso a cobrinha bata em si mesma!#
        if x_novo in lista_cobra:
            game_over(score)
        elif y_novo in lista_cobra:
            game_over(score)

        #colocando os valores novos na lista#
        lista_cobra.append([x_novo, y_novo])
        del lista_cobra[0]

        return dx, dy, lista_cobra, dir


    #Cuida da relação comida ~ cobrinha#
    def verifica_comida(dx, dy, x_comida, y_comida, lista_cobra, score):

        head = lista_cobra[-1]
        x_novo = head[0] + dx
        y_novo = head[1] + dy

        # quando ele come#
        if head[0] == x_comida and head[1] == y_comida:
            lista_cobra.append([x_novo, y_novo])
            x_comida = round(random.randrange(0, 600 - d) / 20) * 20  #gerando novas posições#
            y_comida = round(random.randrange(0, 600 - d) / 20) * 20
            score += 5

        pygame.draw.rect(tela, verde, [x_comida, y_comida, d, d])

        return x_comida, y_comida, lista_cobra, score


    #Loop do jogo#
    while True:
        score_font = font.render(f'{score}', True, (255, 255, 255))  #colocando o score na tela#
        tela.blit(score_font, (290, 0))

        pygame.display.update() #atualiza a tela#

        desenha_cobra(lista_cobra)
        dx, dy, lista_cobra, dir = mover_cobra(dx, dy, lista_cobra, dir)
        x_comida, y_comida, lista_cobra, score = verifica_comida(dx, dy, x_comida, y_comida, lista_cobra, score)

        clock.tick(20)  # atualiza a cada 20 segundos


#chamando o menu, que ou chamará a função que roda o jogo, ou a função de game over
menu()

