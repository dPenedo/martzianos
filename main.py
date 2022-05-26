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

# Agregar Música
def musica_on():
    mixer.music.load('audio/fondo.mp3')
    mixer.music.set_volume(0.6)
    mixer.music.play()


#  Variables Jugador
img_jugador = pygame.image.load("img/cohete-espacial.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
# Puntaje
puntaje = 0

#  Variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y =[]
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8 


for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("img/ufo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50,180))
    enemigo_x_cambio.append(0.6)
    enemigo_y_cambio.append(70)

#  Variables de la bala
img_bala = pygame.image.load("img/bullet.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#fuente = pygame.font.Font('FakeHopeFilled.ttf', 32)

# Texto final de juego
fuente_final = pygame.font.Font('ka1.ttf', 60)
def texto_final():
    mi_fuente_final = fuente_final.render('GAME OVER', True, (237, 235, 220))
    pantalla.blit(mi_fuente_final, (150, 250))

# Funcion mostrar puntaje
fuente = pygame.font.Font('ka1.ttf', 36)
def mostrar_puntaje():
    texto = fuente.render(f'Puntaje: {puntaje}', True, (237, 235, 220))
    pantalla.blit(texto, (15, 20))

# Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Humo
img_humo = pygame.image.load("img/humo.png")
img_explosion = pygame.image.load("img/explosion.png")
def humo(x,y):
    pantalla.blit(img_humo, (x + 20, y - 30))
    pantalla.blit(img_explosion, (x , y - 20))
    pantalla.blit(img_explosion, (x + 20 , y))
    pantalla.blit(img_explosion, (x + 10 , y +20))

# Funcion enemigo
def enemigo(x, y, ene ):
    pantalla.blit(img_enemigo[ene], (x, y))

# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))
# Funcion detectar colisiones

def hay_colision(x_1, y_1, x_2, y_2):
    operacion1= math.pow(x_1 - x_2, 2)
    operacion2= math.pow(y_2 - y_1, 2)
    distancia = math.sqrt(operacion1 + operacion2)
    if distancia < 27:
        return True
    else:
        return False


musica_on()

#Loop del juego
se_ejecuta = True
derrota = False
while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar eventos
    for evento in pygame.event.get():
        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE and bala_visible == False and derrota == False:
                sonido_bala = mixer.Sound('audio/disparo.mp3')
                sonido_bala.play()
                bala_x = jugador_x
                disparar_bala(bala_x, bala_y)
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
            if evento.key == pygame.K_m:
                mixer.music.pause()
            if evento.key == pygame.K_s:
                mixer.music.play()

        # Evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación del jugador
    jugador_x += jugador_x_cambio
    #Mantener en los bordes del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        #Fin del juego


        #if enemigo_y[e] > 500 and int(enemigo_x[e]) == jugador_x_cambio:
            #for k in range(cantidad_enemigos):
            #    enemigo_y[k] = 1000
        enemigo_x[e] += enemigo_x_cambio[e]

    #Mantener en los bordes del enemigo
        if enemigo_x[e]<= 0:
            enemigo_x_cambio[e]= 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

    #Colision
        colision = hay_colision(enemigo_x[e] , enemigo_y[e] , bala_x, bala_y)
        if colision == True:
            sonido_colision = mixer.Sound('audio/golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje +=1
            enemigo_x[e]  = random.randint(0, 736)
            enemigo_y[e]  = random.randint(50,200)
        enemigo(enemigo_x[e], enemigo_y[e], e)
        area_jugador_y = jugador_y - 30
        choque_final = hay_colision(enemigo_x[e], enemigo_y[e], jugador_x, area_jugador_y)
        
        if choque_final:
            sonido_final = mixer.Sound('audio/explosion_final.mp3')
            sonido_final.play(0)
            pygame.mixer.music.stop()
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            derrota = True

    #Movimiento bala
    if bala_y <= -32:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio
        

    jugador(jugador_x, jugador_y)
    #Derrota
    if derrota == True:
        texto_final()
        humo(jugador_x, jugador_y)
        bala_y = -1000

    mostrar_puntaje()
    # actualizar
    pygame.display.update()
