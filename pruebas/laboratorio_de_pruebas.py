import pygame
import math
import random
from pygame import mixer

#Inicializar Pygame
pygame.init()

#Crear la Pantalla
pantalla = pygame.display.set_mode((800,600))

#Título e icono

pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("img/ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('img/fondo-espacio.jpg')
clock = pygame.time.Clock()


fuente_inicio = pygame.font.Font('fonts/ka1.ttf', 76)
def mostrar_inicio():
    texto = fuente_inicio.render('MARTZIANOS', True, (237, 235, 220))
    pantalla.blit(texto, (75, 180))
    texto2 = fuente_inicio.render('WAR', True, (237, 235, 220))
    pantalla.blit(texto2, (280, 280))


fuente = pygame.font.Font('fonts/ka1.ttf', 36)
def mostrar_puntaje(x, y):
    texto = fuente.render('Puntaje:', True, (237, 235, 220))
    pantalla.blit(texto, (x, y))

font_fade = pygame.USEREVENT + 2
pygame.time.set_timer(font_fade, 500)
font = pygame.font.Font('fonts/ka1.ttf', 30)
text_surf = font.render('press  Space  to  start', True, (237, 235, 220))    
show_text = True
def press_space():
    text = font.render('press Space to start', True, (237, 235, 220))
    pantalla.blit(text, (160,450))



fuente = pygame.font.Font('fonts/ka1.ttf', 36)
def texto_aparece():
    texto = fuente.render('Puntaje:', True, (237, 235, 220))
    pantalla.blit(texto, (x, y))


se_ejecuta = True
gameStart = False
while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))
    if not gameStart:
        mostrar_inicio()
        press_space()
    if gameStart == True:
        mostrar_puntaje(15,20)
        #pygame.time.set_timer(texto_aparece, 2000)

    for event in pygame.event.get():
        # Evento cerrar
        if event.type == pygame.QUIT:
            se_ejecuta = False
        if event.type == font_fade:
            show_text = not show_text     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameStart = True

    pygame.display.update()

