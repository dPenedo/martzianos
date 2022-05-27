import pygame
import math
import random
from pygame import mixer

#Starting Pygame
pygame.init()

#Creates the screen
screen = pygame.display.set_mode((800, 600))

#Title and icon

pygame.display.set_caption("Martzianos War")
icon = pygame.image.load("img/ovni.png")
pygame.display.set_icon(icon)
background = pygame.image.load('img/fondo-espacio.jpg')

# Adds Music
def music_on():
    mixer.music.load('audio/fondo.mp3')
    mixer.music.set_volume(0.6)
    mixer.music.play()


#  Variables Jugador
img_player = pygame.image.load("img/cohete-espacial.png")
player_x = 368
player_y = 500
player_x_change = 0
# Puntaje
score = 0

#  Variables enemy
img_enemy = []
enemy_x = []
enemy_y =[]
enemy_x_change = []
enemy_y_change = []
number_enemies = 8


for e in range(number_enemies):
    img_enemy.append(pygame.image.load("img/ufo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 180))
    enemy_x_change.append(0.6)
    enemy_y_change.append(70)

#  Variables of the bullet
img_bala = pygame.image.load("img/bullet.png")
bullet_x = 0
bullet_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bullet_visible = False

# Text of Gamve Over
font_final = pygame.font.Font('ka1.ttf', 60)
def final_text():
    my_font_final = font_final.render('GAME OVER', True, (237, 235, 220))
    screen.blit(my_font_final, (150, 250))

# Function showing score
score_font = pygame.font.Font('ka1.ttf', 36)
def show_score():
    text = score_font.render(f'Puntaje: {score}', True, (237, 235, 220))
    screen.blit(text, (15, 20))

# Function player
def player(x, y):
    screen.blit(img_player, (x, y))


# Broken spaceship on the end
img_smoke = pygame.image.load("img/humo.png")
img_explosion = pygame.image.load("img/explosion.png")
def smoke(x, y):
    screen.blit(img_smoke, (x + 20, y - 30))
    screen.blit(img_explosion, (x , y - 20))
    screen.blit(img_explosion, (x + 20 , y))
    screen.blit(img_explosion, (x + 10 , y + 20))

# Enemy function
def enemy(x, y, ene):
    screen.blit(img_enemy[ene], (x, y))

# Function for shooting bullets
def shooting_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(img_bala, (x + 16, y + 10))
# Funcion detectar colisiones

def colision(x_1, y_1, x_2, y_2):
    operation1= math.pow(x_1 - x_2, 2)
    operation2= math.pow(y_2 - y_1, 2)
    distance = math.sqrt(operation1 + operation2)
    if distance < 27:
        return True
    else:
        return False


music_on()

#Loop of the game
game_runing = True
defeat = False
while game_runing:
    # Background image
    screen.blit(background, (0, 0))

    # Iterate events
    for event in pygame.event.get():
        # Event for quiting
        if event.type == pygame.QUIT:
            game_runing = False
        # Event for pressing keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE and bullet_visible == False and defeat == False:
                sonido_bala = mixer.Sound('audio/disparo.mp3')
                sonido_bala.play()
                bullet_x = player_x
                shooting_bullet(bullet_x, bullet_y)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_m:
                mixer.music.pause()
            if event.key == pygame.K_s:
                mixer.music.play()

        # Event of releasing keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Change players location
    player_x += player_x_change
    # Keep the player on the screen's borders
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Changes enemies location
    for e in range(number_enemies):
        #if enemigo_y[e] > 500 and int(enemigo_x[e]) == jugador_x_cambio:
            #for k in range(cantidad_enemigos):
            #    enemigo_y[k] = 1000
        enemy_x[e] += enemy_x_change[e]

        # Keep the enemies on the screen's borders
        if enemy_x[e]<= 0:
            enemy_x_change[e]= 1
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -1
            enemy_y[e] += enemy_y_change[e]

    #Colision
        colision_enemy_and_bullet = colision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if colision_enemy_and_bullet == True:
            sound_colision = mixer.Sound('audio/golpe.mp3')
            sound_colision.play()
            bullet_y = 500
            bullet_visible = False
            score +=1
            enemy_x[e]  = random.randint(0, 736)
            enemy_y[e]  = random.randint(50, 200)
        enemy(enemy_x[e], enemy_y[e], e)
        player_y_area = player_y - 30
        final_colision = colision(enemy_x[e], enemy_y[e], player_x, player_y_area)
        
        if final_colision:
            final_sound = mixer.Sound('audio/explosion_final.mp3')
            final_sound.play(0)
            pygame.mixer.music.stop()
            for k in range(number_enemies):
                enemy_y[k] = 1000
            defeat = True

    # Bullet's location
    if bullet_y <= -32:
        bullet_y = 500
        bullet_visible = False
    if bullet_visible:
        shooting_bullet(bullet_x, bullet_y)
        bullet_y -= bala_y_cambio
        

    player(player_x, player_y)
    # Defeat
    if defeat == True:
        final_text()
        smoke(player_x, player_y)
        bullet_y = -1000

    show_score()
    # Update
    pygame.display.update()
