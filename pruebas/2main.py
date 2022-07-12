import pygame
import os
import time
import random

pygame.font.init()
WIDTH, HEIGHT  = 800, 600
SCREEN =  pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Martzianos')



# Load images
blue_space_ship = pygame.image.load('img/cohete-espacial.png')
green_space_ship = pygame.image.load('img/cohete-espacial.png')
red_space_ship = pygame.image.load('img/cohete-espacial.png')


#laser

laser_blue = pygame.image.load('img/bullet.png')
laser_green = pygame.image.load('img/bullet.png')
laser_red= pygame.image.load('img/bullet.png')

#Background

Background = pygame.image.load('img/fondo-espacio.jpg')

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("ka1", 50)
    player_vel= 5

    clock = pygame.time.Clock()
    player = Player(300, 500)

    def redraw_window():
        SCREEN.blit(Background,(0,0))
        #draw text
        lives_label = main_font.render(f'lives : {lives}', 1, (255, 0, 0))
        level_label = main_font.render(f'Level : {level}', 1, (255, 255, 255))

        SCREEN.blit(lives_label, (20, 20))
        SCREEN.blit(level_label, (WIDTH - level_label.get_width() -20, 20))
        player.draw(SCREEN)
        pygame.display.update()
        
    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel 
        if keys[pygame.K_RIGHT] and player.x + player_vel +50 < WIDTH:
            player.x += player_vel 
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel 
        if keys[pygame.K_DOWN] and player.y + player_vel +50 < HEIGHT:
            player.y += player_vel 

main()
