from sys import exit
import random

import pygame
from pygame.locals import *


SCREEN_SIZE = (800, 600)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
CLOCK = pygame.time.Clock()
SCORE = 0
LIFE = 3


class Bullet():

    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 24
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return

    def update(self, y_amount=5):
        self.y -= y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


class EnemyBullet():

    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 12
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return

    def update(self, y_amount=5):
        self.y += y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


class Enemy():

    def __init__(self, x_coord, y_coord, points):
        self.x = x_coord
        self.y = y_coord
        self.points = points
        self.image = pygame.image.load('enemy.png')
        self.speed = 3
        return

    def update(self, surface, dirx, y_amount=0):
        self.x += (dirx * self.speed)
        self.y += y_amount
        surface.blit(self.image, (self.x, self.y))
        return


def check_collision(object1_x, object1_y, object2_x, object2_y):
    if ((object1_x > object2_x) and (object1_x < object2_x + 35) and 
        (object1_y > object2_y) and (object1_y < object2_y + 35)
    ):
        return True
    return False

def generate_enemies():
    matrix = []
    for y in range(5):
        if y == 0:
            points = 30
        elif y == 1 or y == 2:
            points = 20
        else:
            points = 10

        enemies = [Enemy(80 + (40 * x), 50 + (50*y), points) for x in range(11)]
        matrix.append(enemies)
    return matrix


class SpaceInvadersGame(object):
    def __init__(self, score=SCORE, life=LIFE):
        pygame.init()
        flag = DOUBLEBUF
        self.surface = pygame.display.set_mode(SCREEN_SIZE, flag)
        self.surface.fill(BLACK)
        myfont = pygame.font.Font(None, 15)
        self.bullets_array = []
        self.enemies_matrix = generate_enemies()
        self.enemies_bullets = []
        self.score = score
        self.life = life


        label = myfont.render("Press ENTER to start game", 1, YELLOW)
        self.surface.blit(label, (100, 100))
        self.draw_player()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.gamestate = 1
                    self.loop()
                if (event.type == QUIT or 
                    (event.type == KEYDOWN and event.key == K_ESCAPE)
                ):
                    exit()

    def game_over_screen(self):
        myfont = pygame.font.Font(None, 15)
        label = myfont.render("Press Y to restart game, N to exit", 1, YELLOW)
        score = myfont.render("You finished with score: {}".format(self.score), 1, YELLOW)
        self.surface.fill(BLACK)
        self.surface.blit(label, (100, 100))
        self.surface.blit(score, (100, 120))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_y:
                    SpaceInvadersGame()
                if (event.type == QUIT or 
                    (event.type == KEYDOWN and event.key == K_ESCAPE) or
                    (event.type == KEYDOWN and event.key == K_n)
                ):
                    exit()

    def continue_screen(self):
        myfont = pygame.font.Font(None, 15)
        label = myfont.render("Press ENTER to continue game", 1, YELLOW)
        score = myfont.render("Your score: {}".format(self.score), 1, YELLOW)
        self.surface.fill(BLACK)
        self.surface.blit(label, (100, 100))
        self.surface.blit(score, (100, 120))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    SpaceInvadersGame(score=self.score, life=self.life)
                if (event.type == QUIT or 
                    (event.type == KEYDOWN and event.key == K_ESCAPE) or
                    (event.type == KEYDOWN and event.key == K_n)
                ):
                    exit()

    def game_exit(self):
        """ funkcja przerywa dzialanie gry i wychodzi do systemu"""
        exit()

    def draw_player(self):
        self.player = pygame.image.load("ship.png")
        self.speed = 5
        self.player_x = SCREEN_SIZE[0]/2 - 25
        self.player_y = SCREEN_SIZE[1] - 75

    def move(self, dirx, diry):
        self.player_x = self.player_x + (dirx * self.speed)
        self.player_y = self.player_y + (diry * self.speed)

    def loop(self):
        """ glowna petla gry """
        can_shoot = True
        fire_wait = 500
        enemy_can_shoot = True
        enemy_fire_wait = 1500
        moving = False
        myfont = pygame.font.Font(None, 20)

        while self.gamestate == 1:
            for event in pygame.event.get():
                if (event.type == QUIT or
                    (event.type == KEYDOWN and event.key == K_ESCAPE)
                ):
                    self.game_exit()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT] and self.player_x < SCREEN_SIZE[0] - 50:
                self.move(1,0)

            if keys[K_LEFT] and self.player_x > 0:
                self.move(-1, 0)

            if keys[K_SPACE] and can_shoot:
                bullet = Bullet(self.surface, self.player_x, self.player_y)
                self.bullets_array.append(bullet)
                can_shoot = False

            if not self.life:
                self.gamestate = 0

            if not can_shoot and fire_wait <= 0:
                can_shoot = True
                fire_wait = 500

            fire_wait -= CLOCK.tick(60)
            enemy_fire_wait -= CLOCK.tick(60)

            self.surface.fill(BLACK)
            self.surface.blit(self.player, (self.player_x, self.player_y))

            for enemies in self.enemies_matrix:
                for enemy in enemies:
                    if enemies[-1].x > 765:
                        dirx = -1
                        moving = True
                        enemy.update(self.surface, 0, 5)
                    elif enemies[0].x < 0:
                        dirx = 1
                        moving = True
                        enemy.update(self.surface, 0, 5)
                    elif not moving:
                        dirx = 1
                    enemy.update(self.surface, dirx)

            if enemy_can_shoot:
                flat_list = [enemy for enemies in self.enemies_matrix for enemy in enemies]
                random_enemy = random.choice(flat_list)
                enemy_bullet = EnemyBullet(self.surface, random_enemy.x, random_enemy.y)
                self.enemies_bullets.append(enemy_bullet)
                enemy_can_shoot = False

            if not enemy_can_shoot and enemy_fire_wait <= 0:
                enemy_fire_wait = 1500
                enemy_can_shoot = True

            for enemy_bullet in self.enemies_bullets:
                enemy_bullet.update()
                if enemy_bullet > 600:
                    self.enemies_bullets.remove(enemy_bullet)

                if (check_collision(enemy_bullet.x, enemy_bullet.y, self.player_x, self.player_y) and
                    enemy_bullet in self.enemies_bullets
                ):
                    self.enemies_bullets.remove(enemy_bullet)
                    self.life -= 1

            for bullet in self.bullets_array:
                bullet.update()
                if bullet.y < 0:
                    self.bullets_array.remove(bullet)

                for enemies in self.enemies_matrix:
                    for enemy in enemies:
                        if (check_collision(bullet.x, bullet.y, enemy.x, enemy.y) 
                            and bullet in self.bullets_array
                        ):
                            self.score += enemy.points
                            enemies.remove(enemy)
                            self.bullets_array.remove(bullet)

            score_label = myfont.render("Score: {}".format(self.score), 1, YELLOW)
            self.surface.blit(score_label, (25, 575))

            life_label = myfont.render("Life: {}".format(self.life), 1, YELLOW)
            self.surface.blit(life_label, (750, 575))

            pygame.display.flip()

            if not any(self.enemies_matrix):
                self.continue_screen()

        self.game_over_screen()

if __name__ == '__main__':
   SpaceInvadersGame()
