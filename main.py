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

# Starting title

starting_font = pygame.font.Font('/fonts/ka1.ttf', 76)
def show_start():
    texto = starting_font.render('MARTZIANOS', True, (237, 235, 220))
    screen.blit(texto, (75, 180))
    texto2 = starting_font.render('WAR', True, (237, 235, 220))
    screen.blit(texto2, (280, 280))


font_fade = pygame.USEREVENT + 2
pygame.time.set_timer(font_fade, 500)
font = pygame.font.Font('/fonts/ka1.ttf', 30)
def press_space():
    text = font.render('press Space to start', True, (237, 235, 220))
    screen.blit(text, (160,450))


# Adds Music
def music_on():
    mixer.music.load('audio/fondo.mp3')
    mixer.music.set_volume(0.6)
    mixer.music.play()

# Score
score = 0
#  Variables Player
img_player = pygame.image.load("img/cohete-espacial.png")
player_x = 368
player_y = 500
player_speed = 3


#  Variables enemy
img_enemy = []
enemy_x = []
enemy_y =[]
enemy_x_change = []
enemy_y_change = []
enemy_speed = 2.5
number_enemies = 8


for e in range(number_enemies):
    img_enemy.append(pygame.image.load("img/ufo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 180))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(70)
#  Variables of the bullet
img_bala = pygame.image.load("img/bullet.png")
bullet_x = 0
bullet_y = 500
bala_x_cambio = 0
bullet_speed = 5
bullet_visible = False

# Text of Game Over
font_final = pygame.font.Font('fonts/ka1.ttf', 60)
def final_text():
    my_font_final = font_final.render('GAME OVER', True, (237, 235, 220))
    screen.blit(my_font_final, (150, 250))

# Function showing score
score_font = pygame.font.Font('fonts/ka1.ttf', 36)
def show_score():
    text = score_font.render(f'Score: {score}', True, (237, 235, 220))
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

FPS=60
clock = pygame.time.Clock()
#Loop of the game
game_runing = True
defeat = False
gameStart = False
while game_runing:
    clock.tick(FPS)
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Event for quiting
        if event.type == pygame.QUIT:
            game_runing = False
    player(player_x, player_y)
 
    keys = pygame.key.get_pressed()
    # Moving controls
    if keys[pygame.K_LEFT] and player_x - player_speed > 0 and gameStart == True:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x - player_speed< 736 and gameStart == True:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y - player_speed > 0 and gameStart == True:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + player_speed < 530 and gameStart == True:
        player_y += player_speed
    # Starting
    if keys[pygame.K_SPACE] and gameStart == False:
        gameStart = True
    #Shoot
    if keys[pygame.K_SPACE] and bullet_visible == False and defeat == False:
        bullet_sound = mixer.Sound('audio/disparo.mp3')
        bullet_sound.play()
        bullet_x = player_x
        bullet_y = player_y
        shooting_bullet(bullet_x, bullet_y)
    # Other controls
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    if keys[pygame.K_m]:
        mixer.music.pause()
    if keys[pygame.K_p]:
        mixer.music.play()
    if not gameStart:
        show_start()
        press_space()
    if gameStart == True:
        show_score()
        for e in range(number_enemies):
            enemy_x[e] += enemy_x_change[e]
            if enemy_x[e]<= 0:
                enemy_x_change[e] += enemy_speed
                enemy_y[e] += random.randint(10,30)
            elif enemy_x[e] >= 736:
                enemy_x_change[e] -= enemy_speed
                enemy_y[e] += random.randint(10, 30)
            
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
                defeat = True
    # Restarting
    if keys[pygame.K_SPACE] and defeat == True:
        defeat = False
        show_score()
        score = 0
        gameStart = True
        player_x = 368
        player_y = 500
        pygame.mixer.music.play()
        for k in range(number_enemies):
            enemy_y[k] -= random.randint(850, 940)

                

    # Iterate events

        

    # Bullet's location
    if bullet_y <= -10:
        bullet_y = player_y
        bullet_visible = False
    if bullet_visible:
        shooting_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        

    # Update
    pygame.display.update()
