from calendar import c
import pygame, fractions
from random import choice, randint, shuffle
import numpy as np
pygame.init()
pygame.font.init()

FPS = 60
TAM = 32
RES = [28*TAM, 15*TAM]

#Colors Const
WHITE = (240, 240, 200)
BLACK = (20, 20, 20)
PINK = (255, 190, 210)
GREEN = (190, 255, 180)
BLUE = (190, 255, 255)

SINAIS = ["+", "-"]
ABCW = ['a', 'b', 'c', 'd', 'e', 'x', 'y', 'w', 'z']
MIN = -10
MAX = 10


def solucao(A, B):
    try:
        invA = np.linalg.inv(A)
        return np.dot(invA, B)
    except:
        return "Sem solução pelo metodo utilizado"


def gerarSistema(n=2):
    nEq = n
    nTe = n
    nIc = n

    a = []
    for n in range(nEq):
        termo = []
        for i in range(nTe):
            p = 0
            while p == 0:
                p = randint(MIN, MAX)
            termo.append(p)
        a.append(termo)

    b = []
    for n in range(nEq):
        i = 0
        while i == 0:
            i = randint(MIN, MAX)
        b.append(i)
    
    x = []
    for n in range(nIc):
        k = choice(ABCW)
        while k in x:
            k = choice(ABCW)
        x.append(k)

    sistema = []
    eq = []
    for n in range(nEq):
        for i in range(len(x)):
            if a[n][i] > 0:
                eq.append('+' + str(a[n][i]) + x[i])
            else:
                eq.append(str(a[n][i]) + x[i])
        
        eq = ' '.join(str(thing) for thing in eq) + " =" + " " + str(b[n])
        sistema.append(eq)
        eq = []
        shuffle(x)

    a = np.array(a) 
    b = np.array(b)
    
    return sistema, a, b, x
    
def checkPos(btn):
    mousePos = pygame.mouse.get_pos()
    if mousePos[0] > btn.x and mousePos[0] < btn.x + btn.width:
        if mousePos[1] > btn.y and mousePos[1] < btn.y + btn.height:
            return True

def drawBtn(surf, btn1, btn2, font):
    pygame.draw.rect(surf, BLUE, btn1)
    pygame.draw.rect(surf, PINK, btn2)

    txtMais = font.render("+", 1, BLACK)
    txtMenos = font.render("-", 1, BLACK)
    #896, 480
    surf.blit(txtMais, (877, 4))
    surf.blit(txtMenos, (877, 53))

def ui(surf, font, clock, sis, res, x, n):
    txtFps = font.render("FPS: " + str(int(clock.get_fps())), 1, WHITE)
    surf.blit(txtFps, (0, 0))
    txtN = font.render('N: ' + str(n), 1, WHITE)
    surf.blit(txtN, (0+txtFps.get_width()+16, 0))

    if sis != None:
        for s in range(len(sis)):
            txtSis = font.render(sis[s], 1, WHITE)
            surf.blit(txtSis, (0, 100 + (TAM*s//1.5)))


    try:
        a = []
        for i in range(len(x)):
            a.append(x[i] + " = " + str(fractions.Fraction(round(res[i], 3)).limit_denominator()))
        a = ' '.join(str(j) for j in a)
        
    
    except:
        a = "Não foi possível resolver"

    txtRes = font.render(a, 1 , GREEN)
    surf.blit(txtRes, (0, RES[1]-txtRes.get_height()))
    

def main():
    run = True
    win = pygame.display.set_mode((RES[0], RES[1]))
    clock = pygame.time.Clock()
    pygame.display.set_caption("hihihihihihihihihih")
    myFont = pygame.font.SysFont("Comic Sans MS", TAM//2)
    sis = None
    res = None
    a = None
    b = None
    x = None
    n = 2
    btnMais = pygame.Rect(RES[0]-TAM, 0, TAM, TAM)
    btnMenos = pygame.Rect(RES[0]-TAM, TAM+TAM/2, TAM, TAM)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_r:
                    sis, a, b, x = gerarSistema(n)
                    res = solucao(a, b)
                if event.key== pygame.K_KP_PLUS:
                    if n < 9:
                        n += 1
                if event.key == pygame.K_KP_MINUS:
                    if n > 2:
                        n -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if checkPos(btnMais):
                        if n < 9:
                            n += 1
                    if checkPos(btnMenos):
                        if n > 2:
                            n -= 1
                    

        drawBtn(win, btnMais, btnMenos, myFont)
        ui(win, myFont, clock, sis, res, x, n)
        pygame.display.update()
        win.fill(BLACK)
        clock.tick(FPS)

main()