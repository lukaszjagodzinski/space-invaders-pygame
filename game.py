from sys import exit    
import random               #importing random library, necessary for generating random enemies throughout the game

import pygame               #making use of all the availble pygame modules 
from pygame.locals import *

SCREEN_SIZE = (800, 600)    #setting up the game at original state for window size, players, time, score and life
GREEN = (0, 255, 0)         #necessary for the start of the game
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
CLOCK = pygame.time.Clock()
SCORE = 0
LIFE = 3

#bullets class for the user, deals with position and visual image of bullets
class Bullet():                                         
    def __init__(self, surface, x_coord, y_coord):      #setting the position of bullets and loading the image for visuals 
        self.surface = surface
        self.x = x_coord + 24
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return

    def update(self, y_amount=5):   
        self.y -= y_amount                              #updating/decrementing amount of bullets left
        self.surface.blit(self.image, (self.x, self.y)) #updates the position of the laser, appears to have the laser moving
        return

#bullets class for enemy, deals with position and visual image for oponent
class EnemyBullet():                                    
    def __init__(self, surface, x_coord, y_coord):      #same idea to the bullets class, but for enemys 
        self.surface = surface
        self.x = x_coord + 12
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return

    def update(self, y_amount=5):
        self.y += y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return

#drawing the enemy and placement of the enemy, includes movement
class Enemy():                                      
    def __init__(self, x_coord, y_coord, points):   #placement of enemy, in terms of x and y coords  
        self.x = x_coord
        self.y = y_coord
        self.points = points
        self.image = pygame.image.load('enemy.png') #upload image of enemy onto the screen
        self.speed = 3                              #setting the speed of the enemy's movement, helps change the position
        return

    def update(self, surface, dirx, y_amount=0):    #updating the movement of the enemy
        self.x += (dirx * self.speed)               #multiplying the x value by the speed, increasing the x value by 3 each time
        self.y += y_amount
        surface.blit(self.image, (self.x, self.y))  #movement of enemy, drawing the same image onto itself, according to the 
                                                    #x and y position
        return

#checking to see if two objects collide with one another
def check_collision(object1_x, object1_y, object2_x, object2_y):
    if ((object1_x > object2_x) and (object1_x < object2_x + 35) and 
        (object1_y > object2_y) and (object1_y < object2_y + 35)
    ):
        return True
    return False

def generate_enemies():         #creating the enemies, in a 1D array    *******************************
    matrix = []
    for y in range(5):          #looping through the enemies, assigning points on difficulty for player to be rewarded 
        if y == 0:
            points = 30         #giving the enemies of higher position (closer to the very top) more points rewarded 
        elif y == 1 or y == 2:  
            points = 20         
        else:
            points = 10

        enemies = [Enemy(80 + (40 * x), 50 + (50*y), points) for x in range(11)]
        matrix.append(enemies)
    return matrix

class SpaceInvadersGame(object):
    def __init__(self, score=SCORE, life=LIFE):                     #setting up the initial game, window screen user will see
                                                                    #and other necessary starting values 
        pygame.init()                                               #initialize all imported pygame modules
        flag = DOUBLEBUF                                            #setting up double buffered video mode, draws all the
                                                                    #routines and then copies it into video memory, helps avoid
                                                                    #flickering between screens as other routines are drawn
        self.surface = pygame.display.set_mode(SCREEN_SIZE, flag)   
        self.surface.fill(BLACK)                                    #initializing all the start values of the beginning of game
        myfont = pygame.font.Font(None, 15)
        self.bullets_array = []                                     
        self.enemies_matrix = generate_enemies()                    
        self.enemies_bullets = []
        self.score = score
        self.life = life

        label = myfont.render("Press ENTER to start game", 1, YELLOW) 
        self.surface.blit(label, (100, 100))
        self.draw_player()
        pygame.display.flip()                                       #updating the display surface to screen, after drawing 

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:     #hitting the enter key; setting bool to true, to start game 
                    self.gamestate = 1
                    self.loop()                                         #calling the function that takes care of the state of game
                if (event.type == QUIT or                               #taking in the keyboard input, exiting the game if
                    (event.type == KEYDOWN and event.key == K_ESCAPE)   #user presses escape key
                ):
                    exit()

    def game_over_screen(self):                 #displaying the end result, and actions that can be done after the game is complete
        myfont = pygame.font.Font(None, 15)
        label = myfont.render("Press Y to restart game, N to exit", 1, YELLOW)
        score = myfont.render("You finished with score: {}".format(self.score), 1, YELLOW)
        self.surface.fill(BLACK)
        self.surface.blit(label, (100, 100))    #displaying the instructions for restarting or exiting game
        self.surface.blit(score, (100, 120))
        pygame.display.flip()                   #updating display screen to show new instructions available to user
        
        while True:             
            for event in pygame.event.get():                                #taking in the keyboard input to decide on next action
                if event.type == KEYDOWN and event.key == K_y:              #if user decides to play a new game, run the whole
                    SpaceInvadersGame()                                     #game again by calling the main function
                if (event.type == QUIT or 
                    (event.type == KEYDOWN and event.key == K_ESCAPE) or    #exit the game if user decides to not play a new game
                    (event.type == KEYDOWN and event.key == K_n)
                ):
                    exit()

    def continue_screen(self):                  #continuation screen, displays the next actions available to move on
        myfont = pygame.font.Font(None, 15)
        label = myfont.render("Press ENTER to continue game", 1, YELLOW)
        score = myfont.render("Your score: {}".format(self.score), 1, YELLOW)
        self.surface.fill(BLACK)
        self.surface.blit(label, (100, 100))
        self.surface.blit(score, (100, 120))
        pygame.display.flip()           #updating the display screen to show new instructions to continue or exit game
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    SpaceInvadersGame(score=self.score, life=self.life)
                if (event.type == QUIT or                                   #user decides to not continue playing, exits
                    (event.type == KEYDOWN and event.key == K_ESCAPE) or
                    (event.type == KEYDOWN and event.key == K_n)
                ):
                    exit()

    def game_exit(self):
        """ funkcja przerywa dzialanie gry i wychodzi do systemu""" 
        exit()                                      #function interrupts the action of the game and goes into the system

    def draw_player(self):                          #function to render player, to be drawn on the display screen
        self.player = pygame.image.load("ship.png") #upload image of player to be displayed, set speed and size 
        self.speed = 5
        self.player_x = SCREEN_SIZE[0]/2 - 25
        self.player_y = SCREEN_SIZE[1] - 75

    def move(self, dirx, diry):
        self.player_x = self.player_x + (dirx * self.speed)     #changing the player's position through speed, direction
        self.player_y = self.player_y + (diry * self.speed)     #and current position in terms of x and y coords

    def loop(self):
        """ glowna petla gry """                #main loop of game
        can_shoot = True                        #setting booleans to restrict the user from shooting if they run out of bullets
        fire_wait = 500                         #necessary for restricting player from continously shooting, reload timer
        enemy_can_shoot = True
        enemy_fire_wait = 1500
        moving = False
        myfont = pygame.font.Font(None, 20)

        while self.gamestate == 1:                                      #as long as the game is in play
            for event in pygame.event.get():                            #taking in keyboard input, to determine next move
                if (event.type == QUIT or
                    (event.type == KEYDOWN and event.key == K_ESCAPE)   #user can exit
                ):
                    self.game_exit()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT] and self.player_x < SCREEN_SIZE[0] - 50:   #or move between left and right on the screen
                self.move(1,0)

            if keys[K_LEFT] and self.player_x > 0:
                self.move(-1, 0)

            if keys[K_SPACE] and can_shoot:
                bullet = Bullet(self.surface, self.player_x, self.player_y)     
                self.bullets_array.append(bullet)                       #user is shooting, takes into consideration position
                can_shoot = False                                       #restricting user from shooting again

            if not self.life:   
                self.gamestate = 0

            if not can_shoot and fire_wait <= 0:    #resetting user's shooting, dependent on the timer set at the beginning
                can_shoot = True                    #allows user to shoot again and resets timer
                fire_wait = 500

            fire_wait -= CLOCK.tick(60)             #decrementing timer to help with buffer on shooting for both players
            enemy_fire_wait -= CLOCK.tick(60)

            self.surface.fill(BLACK)
            self.surface.blit(self.player, (self.player_x, self.player_y)) 

            for enemies in self.enemies_matrix:             #movement of the enemies, depending on which were generated
                for enemy in enemies:
                    if enemies[-1].x > 765:                 #enemies will move in the left direction of x axis
                        dirx = -1
                        moving = True
                        enemy.update(self.surface, 0, 5)    
                    elif enemies[0].x < 0:                  #enemies will move in the right direction of x axis
                        dirx = 1
                        moving = True
                        enemy.update(self.surface, 0, 5)
                    elif not moving:
                        dirx = 1
                    enemy.update(self.surface, dirx)

            if enemy_can_shoot:
                flat_list = [enemy for enemies in self.enemies_matrix for enemy in enemies]   #randomly selecting enemy to shoot
                random_enemy = random.choice(flat_list)                                       #from the available generated enemies
                enemy_bullet = EnemyBullet(self.surface, random_enemy.x, random_enemy.y)
                self.enemies_bullets.append(enemy_bullet)
                enemy_can_shoot = False                                                       #restricting enemy shooting

            if not enemy_can_shoot and enemy_fire_wait <= 0:    #resetting enemy's shooting, if timer ran out
                enemy_fire_wait = 1500
                enemy_can_shoot = True

            for enemy_bullet in self.enemies_bullets:              #removing the bullet after it exceeds the screen in y dir
                enemy_bullet.update()                              #so that the bullet is restricted in terms of the screen size
                if enemy_bullet > 600:
                    self.enemies_bullets.remove(enemy_bullet)

                if (check_collision(enemy_bullet.x, enemy_bullet.y, self.player_x, self.player_y) and
                    enemy_bullet in self.enemies_bullets            #checking to see if the enemy's bullet hit player, if yes
                ):                                                  #then hit is successful and a life is lost
                    self.enemies_bullets.remove(enemy_bullet)
                    self.life -= 1

            for bullet in self.bullets_array:           #updating and restricting the position of the bullet, removing after it 
                bullet.update()                         #passes the screen size in the y direction
                if bullet.y < 0:
                    self.bullets_array.remove(bullet)

                for enemies in self.enemies_matrix:
                    for enemy in enemies:
                        if (check_collision(bullet.x, bullet.y, enemy.x, enemy.y) #checking to see if user's bullet hit enemy
                            and bullet in self.bullets_array                      #if yes, "kill" enemy and remove from screen
                        ):
                            self.score += enemy.points                            #update points/score user receives
                            enemies.remove(enemy)
                            self.bullets_array.remove(bullet)                     

            score_label = myfont.render("Score: {}".format(self.score), 1, YELLOW)
            self.surface.blit(score_label, (25, 575))

            life_label = myfont.render("Life: {}".format(self.life), 1, YELLOW)
            self.surface.blit(life_label, (750, 575))

            pygame.display.flip()               #updating display screen to show the actions of playing the game

            if not any(self.enemies_matrix):    #display the next set of instructions, once all enemies are defeated
                self.continue_screen()

        self.game_over_screen()     

if __name__ == '__main__':
   SpaceInvadersGame()      #running the main function of the loop, to start the game