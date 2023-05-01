import time
import random

import pygame.sprite
from pygame import mixer
pygame.font.init()

from Levels import *
from Animations import *

pygame.init()

# what level is being selected
start_menu = True
level_select = False
level_1 = False
level_2 = False
game_paused = False
playing_game = False
player_move = False
current_level = 0  # 0 is level 1, 1 is level 2
game_over = False

# slows down the animations
start_frame = time.time()
noi = 6
frames_per_second = 10

# screen variables
pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate
font = pygame.font.Font(None, 40)
background_scroll = 0  # controls the parallax background
my_font = pygame.font.SysFont(None, 30)  # sets a font for easy use

# screen flipping variables
gravity = 1  # 1 has the player at the bottom, 2 has the player at the top
cool_down_GC = 300  # gravity change cool downtime

# player variables
bullet_speed = -5
key = pygame.key.get_pressed()  # to avoid having to write the whole thing out each time a key is pressed
score = 0
score_increment = 10



def score_increase():
    global score
    global score_increment

    score += score_increment


# causes the background to move with the player
def parallax_background():
    for repeat in range(5):  # makes sure the background will repeat when it ends
        scroll_speed = 1
        for image in background_images:  # will scroll for every image that the background is made up of
            screen.blit(image, ((repeat * background_width) - background_scroll * scroll_speed, 0))


# the player class
class Player(pygame.sprite.Sprite):
    global gravity

    def __init__(self, player_x, player_y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = idle_images[0]
        self.y_velocity = 5
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.current_health = 1000
        self.max_health = 1000
        self.health_ratio = self.max_health / 400  # sets up the health bar
        self.last_shot = pygame.time.get_ticks()  # keeps track of when the player last shot so they can't shoot constantly
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0  # animation frames
        self.direction = False  # True is left, False is Right
        self.gravity_position = False  # True is the roof, False is the floor
        self.speed = 0  # the players speed

    def update(self):

        # global variables
        global bullet_speed, key, player_move, background_scroll, run, game_over

        # setting speed and cool down rate
        speed = 0
        cool_down = 500  # milliseconds

        # making the health bar update
        self.health_bar()

        # setting the y position of the player to be the y velocity
        self.rect.y += self.y_velocity

        # movement inputs for when the player is able to move
        if key[pygame.K_a] and self.rect.left > 0 and player_move is True and background_scroll > 0:
            if self.y_velocity == 0:  # if the player is on the fround the will go faster
                speed -= 4  # changes the players speed
            if self.y_velocity != 0:  # if the player is in the air the will go slower
                speed -= 3  # changes the players speed
            background_scroll += -1  # changes the background when the player moves
            self.direction = True  # sets the direction the player is going so that the animation can change
        if key[pygame.K_d] and self.rect.right < screen_width and player_move is True and background_scroll < 3000:
            if self.y_velocity == 0:  # if the player is on the fround the will go faster
                speed += 4  # changes the players speed
            if self.y_velocity != 0:  # if the player is in the air the will go slower
                speed += 3  # changes the players speed
            background_scroll += 1  # changes the background when the player moves
            self.direction = False  # sets the direction the player is going so that the animation can change

        # sets time_now to be the current amount of time within the game
        time_now = pygame.time.get_ticks()

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 1 and key[pygame.K_SPACE] and time_now - self.last_shot > cool_down and self.y_velocity == 0\
                and player_move is True:
            bullet = Bullets(self.rect.centerx + 10, self.rect.top)
            bullet_group.add(bullet)  # spawns the bullets, adding them to the bullet group so they can deal damage
            self.last_shot = time_now  # sets last_shot to time_now in order to limit the amount of shots the player has

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 2 and key[pygame.K_SPACE] and time_now - self.last_shot > cool_down and self.y_velocity == 0\
                and player_move is True:
            bullet = Bullets(self.rect.centerx + 10, self.rect.bottom)
            bullet_group.add(bullet)  # spawns the bullets, adding them to the bullet group so they can deal damage
            self.last_shot = time_now  # sets last_shot to time_now in order to limit the amount of shots the player has

        # changes the way the player is falling when the gravity is changed
        if gravity == 1 and player_move is True:
            self.y_velocity += 1
            # if the velocity goes beyond 5 it will set it back to 5
            if self.y_velocity > 5:
                self.y_velocity = 5

        # changes the way the player is falling when the gravity is changed
        if gravity == 2 and player_move is True:
            self.y_velocity += 1
            # if the velocity goes beyond -5 it will set it back to -5
            if self.y_velocity > -5:
                self.y_velocity = -5

        # adds all tilemaps to the level variable
        level = [level1.tile_list, level2.tile_list]

        # checking for collision
        for tile in level[current_level]:

            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + speed, self.rect.y, self.width, self.height):
                speed = 0

            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                if self.y_velocity == 5:
                    self.y_velocity = tile[1].bottom - self.rect.top
                    self.y_velocity = 0
                # check if above the ground
                if self.y_velocity >= 0:
                    self.y_velocity = 0

                # checks for collision in y direction when the gravity has been flipped
                if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                    if self.y_velocity == -5:
                        self.y_velocity = 0
                    # check if above the ground
                    if self.y_velocity <= 0:
                        # stops the player from moving if they hit it
                        self.y_velocity = tile[1].top - self.rect.bottom
                        self.y_velocity = 0

        if level_1 is True:  # will only happen during level 1
            # check for collision with spikes
            if pygame.sprite.spritecollide(self, spike_group, False) and player_move is True:
                self.get_damage(10)  # deals damage
                # if the player stands on it they will stop moving, instead of falling through
                self.y_velocity = tile[1].top - self.rect.bottom
                self.y_velocity = 0

            # check for collision with the flying enemy type, dealing damage when it hits
            if pygame.sprite.spritecollide(self, roof_enemy_group, False) and player_move is True:
                self.get_damage(10)

            # check for collision with the ground enemy type, dealing damage when it hits
            if pygame.sprite.spritecollide(self, ground_enemy_group, False) and player_move is True:
                self.get_damage(10)

            # check the player has reached the end and ending the game when they have
            if pygame.sprite.spritecollide(self, complete_level_group, False) and player_move is True:
                text = font.render('Level Complete', True, 'white')
                screen.blit(text, (925, 372))  # displays font
                game_over = True

        if level_2 is True:  # will only happen during level 2
            # check for collision with spikes
            if pygame.sprite.spritecollide(self, spike_group_2, False) and player_move is True:
                self.get_damage(10)  # deals damage
                # if the player stands on it they will stop moving, instead of falling through
                self.y_velocity = tile[1].top - self.rect.bottom
                self.y_velocity = 0

            # check for collision with the flying enemy type, dealing damage when it hits
            if pygame.sprite.spritecollide(self, roof_enemy_group_2, False) and player_move is True:
                self.get_damage(10)

            # check for collision with the ground enemy type, dealing damage when it hits
            if pygame.sprite.spritecollide(self, ground_enemy_group_2, False) and player_move is True:
                self.get_damage(10)

            # check the player has reached the end and ending the game when they have
            if pygame.sprite.spritecollide(self, complete_level_group_2, False) and player_move is True:
                text = font.render('Level Completed...Ending game...', True, 'white')
                screen.blit(text, (925, 372))  # displays font
                game_over = True

        self.rect.x += speed  # sets the x rect of the player to the speed

        # idle animation when the player is not moving
        if self.y_velocity == 0 and speed == 0 and player_move is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(idle_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = idle_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # running animation when the player is moving
        if self.y_velocity == 0 and speed != 0 and player_move is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(run_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = run_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # falling animation
        if self.y_velocity != 0 and player_move is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(falling_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = falling_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # upside down idle animation when the player is not moving
        if self.y_velocity == 0 and speed == 0 and player_move is True and self.gravity_position is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(USD_idle_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = USD_idle_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # upside down running animation when the player is moving
        if self.y_velocity == 0 and speed != 0 and player_move is True and self.gravity_position is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(USD_run_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = USD_run_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # upside down falling animation
        if self.y_velocity != 0 and player_move is True and self.gravity_position is True:
            self.value += 1  # cycles through the animation frames
            if self.value >= len(USD_falling_images):  # if the animation frame reaches the amount that there are:
                self.value = 0  # sets the frame back to zero
            self.image = USD_falling_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # plays the death animation if the player runs out of health
        if self.current_health <= 0:
            if self.gravity_position is False:  # checks which version of the animation should play
                self.value += 1  # cycles through the animation frames
                if self.value >= len(death_images):  # if the animation frame reaches the amount that there are:
                    self.value = 0  # sets the frame back to zero
                    run = False  # stops the game from running
                self.image = death_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

            # plays the death animation if the self runs out of health
            if self.gravity_position is True:  # checks which version of the animation should play
                self.value += 1  # cycles through the animation frames
                if self.value >= len(USD_death_images):  # if the animation frame reaches the amount that there are:
                    self.value = 0  # sets the frame back to zero
                    run = False  # stops the game from running
                self.image = USD_death_images[self.value]  # sets the player image to the frame that is currently being called
            self.value = int((time.time() - start_frame) * frames_per_second % noi)  # slows the animations down

        # changes the direction of the player sprite based on the way they are walking
        if self.direction is True and player_move is True:
            player.image = pygame.transform.flip(player.image, True, False)

        # checks if the players health goes over the max amount of health the player can have
        if self.current_health >= self.max_health:
            self.current_health = self.current_health

        # deals damage if the player goes off screen
        if self.rect.bottom >= screen_height or self.rect.top <= 0:
            self.current_health -= 50

        # sets self.speed to the players speed
        self.speed = speed

        # update scroll based on player position
        if (self.rect.right > screen_width - 64 and background_scroll < (500 * tile_size) - screen_width) \
                or (self.rect.left < 64 and background_scroll > abs(self.speed)):
            self.rect.x -= self.speed

    def get_damage(self, amount):

        # takes a chosen amount of health each time the function is called
        if self.current_health > 0 and player_move is True:
            self.current_health -= amount
        # will set the health back to zero if it goes under
        if self.current_health <= 0 and player_move is True:
            self.current_health = 0

    def health_bar(self):
        # draws the health bar on screen
        pygame.draw.rect(screen, (255, 87, 51), (10, 10, self.current_health / self.health_ratio, 35))
        pygame.draw.rect(screen, (170, 40, 10), (10, 10, 400, 35), 4)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, bullet_x, bullet_y):
        # sets up all the bullets variables
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = [bullet_x, bullet_y]

    def update(self):

        # destroys the bullets if they go off screen
        self.rect.y += bullet_speed
        if self.rect.bottom > screen_height:  # checking the bottom of the screen
            self.kill()
        if self.rect.top < 0:  # checking the top
            self.kill()


def gravity_change():
    # global variables
    global gravity, bullet_speed, key, cool_down_GC

    # gives switching gravity a cool down in order to stop it being spammed
    cool_down_GC += clock.get_time()
    if cool_down_GC > 300:
        cool_down_GC = 0

    # sets the gravity and changes the bullet speed
    # also sets the player variables on whether or not the player is falling
    # flips the player animations as well
    if key[pygame.K_s] and gravity == 2 and cool_down_GC == 0 and player_move is True:
        gravity = 1
        bullet_speed = -5
        player.gravity_position = False
        player.image = pygame.transform.flip(player.image, False, True)
        bullet_group.empty()

    # sets the gravity and changes the bullet speed
    # also sets the player variables on whether or not the player is falling
    # flips the player animations as well
    if key[pygame.K_w] and gravity == 1 and cool_down_GC == 0 and player_move is True:
        gravity = 2
        bullet_speed = 5
        player.gravity_position = True
        player.image = pygame.transform.flip(player.image, False, True)
        bullet_group.empty()


# sets the cool down to 0
cool_down_GC = 0


# menus
def draw_pause():

    global game_paused, start_menu, run, playing_game, level_1, level_2, player_move

    # draws the menus backing box on screen
    pygame.draw.rect(screen, (24, 20, 37), [810, 325, 300, 220], 0, 15)

    # resume game button
    resume_button = pygame.draw.rect(screen, (181, 80, 136), [830, 350, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 350, 260, 70], 5, 15)
    text = font.render('Resume', True, 'black')
    screen.blit(text, (900, 372))

    # exit game button
    exit_button = pygame.draw.rect(screen, (181, 80, 136), [830, 450, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 450, 260, 70], 5, 15)
    text = font.render('Exit', True, 'black')
    screen.blit(text, (930, 472))

    # checks which button is hovered over when the mouse is clicked
    for pause in pygame.event.get():
        if pause.type == pygame.MOUSEBUTTONDOWN:
            if pause.button == 1:
                # resumes the game
                if resume_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    game_paused = False
                    playing_game = True
                    player_move = True
                # exits the game
                if exit_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    run = False
                else:
                    run = True


def draw_start_menu():

    global game_paused, start_menu, level_select, level_1, run

    # draws backing square for the menu
    pygame.draw.rect(screen, (24, 20, 37), [810, 325, 300, 220], 0, 15)

    # start menu button
    start_button = pygame.draw.rect(screen, (181, 80, 136), [830, 350, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 350, 260, 70], 5, 15)
    text = font.render('Start', True, 'black')
    screen.blit(text, (925, 372))

    # exit game button
    exit_button = pygame.draw.rect(screen, (181, 80, 136), [830, 450, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 450, 260, 70], 5, 15)
    text = font.render('Exit', True, 'black')
    screen.blit(text, (930, 472))

    # checks which button is hovered over when the mouse is clicked
    for start in pygame.event.get():
        if start.type == pygame.MOUSEBUTTONDOWN:
            if start.button == 1:
                # sends the player to the level select screen
                if start_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    pygame.time.delay(500)
                    level_select = True
                    start_menu = False
                    game_paused = False
                # exits the game
                if exit_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    run = False
                else:
                    run = True


def draw_level_select():

    global level_1, level_2, start_menu, level_select, playing_game, player_move

    # draws backing square for the menu
    pygame.draw.rect(screen, (24, 20, 37), [810, 280, 300, 310], 0, 15)

    # start menu button
    level1_button = pygame.draw.rect(screen, (181, 80, 136), [830, 300, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 300, 260, 70], 0, 15)
    text = font.render('Level 1', True, 'black')
    screen.blit(text, (910, 322))

    # back button
    back_button = pygame.draw.rect(screen, (181, 80, 136), [830, 500, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 500, 260, 70], 5, 15)
    text = font.render('Back', True, 'black')
    screen.blit(text, (930, 522))

    # start menu button
    level2_button = pygame.draw.rect(screen, (181, 80, 136), [830, 400, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 400, 260, 70], 0, 15)
    text = font.render('Level 2', True, 'black')
    screen.blit(text, (910, 422))

    # checks which button is hovered over when the mouse is clicked
    for select in pygame.event.get():
        if select.type == pygame.MOUSEBUTTONDOWN:
            if select.button == 1:

                if level1_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    # runs the levels, and the game while stopping the other menus from appearing
                    # also sets the player up in their beginning position while giving them max health
                    level_1 = True
                    level_select = False
                    playing_game = True
                    player_move = True
                    start_menu = False
                    player.rect.x = 64
                    player.rect.y = screen_height - 200
                    player.current_health = player.max_health

                if level2_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    # runs the levels, and the game while stopping the other menus from appearing
                    # also sets the player up in their beginning position while giving them max health
                    level_2 = True
                    level_select = False
                    playing_game = True
                    player_move = True
                    start_menu = False
                    player.rect.x = 64
                    player.rect.y = screen_height - 200
                    player.current_health = player.max_health

                if back_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    # takes the player back to the start menu
                    start_menu = True
                    level_select = False


# puts the player in a group
player_group = pygame.sprite.Group()
player = Player(int(screen_width / 4), screen_height - 500)
player_group.add(player)

# puts the bullets in a group
bullet_group = pygame.sprite.Group()


class GroundEnemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_idle_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.y_velocity = 5
        self.current_health = 50
        self.max_health = 50
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0
        self.move_counter = 0
        self.move_direction = 1

    def update(self):

        # will only happen if the game is not paused
        if game_paused is False:

            # the enemy will move side to side
            self.rect.x += self.move_direction
            self.move_counter -= 1
            if abs(self.move_counter) > 150:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

            # moves the player with the tilemap
            if player.speed == 0:
                self.rect.x -= 0
            if player.speed != 0:
                self.rect.x -= player.speed

            # sets the y rect to the velocity
            self.rect.y += self.y_velocity

            # if the player is moving:
            if player_move is True:
                self.y_velocity += 1
                # if the velocity goes beyond 5 it will set it back to 5
                if self.y_velocity > 5:
                    self.y_velocity = 5

            # easy reference to both levels
            level = [level1.tile_list, level2.tile_list]

            # checking for collision
            for tile in level[current_level]:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    self.move_direction *= -1

                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                    if self.y_velocity == 5:
                        self.y_velocity = tile[1].bottom - self.rect.top
                        self.y_velocity = 0
                    # check if above the ground
                    if self.y_velocity >= 0:
                        self.y_velocity = 0

                    # checks for collision in y direction when the gravity has been flipped
                    if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                        if self.y_velocity == -5:
                            self.y_velocity = 0

                        # check if above the ground
                        if self.y_velocity <= 0:
                            self.y_velocity = tile[1].top - self.rect.bottom
                            self.y_velocity = 0

            # idle animation when the enemy is not moving
            if self.y_velocity == 0 and self.move_counter == 0:
                self.value += 1
                if self.value >= len(enemy_idle_images):
                    self.value = 0
                self.image = enemy_idle_images[self.value]
                self.value = int((time.time() - start_frame) * frames_per_second % noi)

            # running animation when the enemy is moving
            if self.y_velocity == 0 and self.move_counter != 0:
                self.value += 1
                if self.value >= len(enemy_run_images):
                    self.value = 0
                self.image = enemy_run_images[self.value]
                self.value = int((time.time() - start_frame) * frames_per_second % noi)

            # changes the direction of the player sprite based on the way they are walking
            if self.move_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # will take away 10 health if hit by a bullet
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.current_health -= 10
                bullet_group.remove()

            # if the health hits 0 it will kill the enemy
            if self.current_health <= 0:
                score_increase()
                self.kill()


class RoofEnemies(pygame.sprite.Sprite):
    def __init__(self, enemy2_x, enemy2_y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = roof_enemy_run_images[0]
        self.rect = self.image.get_rect()
        self.y_velocity = 5
        self.rect.x = enemy2_x
        self.rect.y = enemy2_y
        self.current_health = 50
        self.max_health = 50
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0
        self.move_counter = 0
        self.move_direction = 1

    def update(self):

        # will only happen if the game is not paused
        if game_paused is False:

            # the enemy will move side to side
            self.rect.x += self.move_direction
            self.move_counter -= 1
            if abs(self.move_counter) > 150:
                self.move_direction *= -1
                self.move_counter *= self.move_direction

            # moves the enemy with the tilemap
            if player.speed == 0:
                self.rect.x -= 0
            if player.speed != 0:
                self.rect.x -= player.speed

            # running animation when the enemy is moving
            if self.move_counter != 0:
                self.value += 1
                if self.value >= len(roof_enemy_run_images):
                    self.value = 0
                self.image = roof_enemy_run_images[self.value]
                self.value = int((time.time() - start_frame) * frames_per_second % noi)

            # changes the direction of the player sprite based on the way they are walking
            if self.move_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        # will take away 10 health if hit by a bullet
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.current_health -= 10
            bullet_group.remove()

        # if the health hits 0 it will kill the enemy
        if self.current_health <= 0:
            score_increase()
            self.kill()


# spikes that will deal damage to the player when stood on
class Spike(pygame.sprite.Sprite):
    # the variables for the spikes
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spikes = pygame.image.load('Graphics/Spike.png')
        self.image = pygame.transform.scale(spikes, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # moves the spikes with the tilemap
        if player.speed == 0:
            self.rect.x -= 0
        if player.speed != 0:
            self.rect.x -= player.speed


class LevelComplete(pygame.sprite.Sprite):
    # the variables for the level complete
    def __init__(self, spike_x, spike_y):
        pygame.sprite.Sprite.__init__(self)
        spikes = pygame.image.load('Graphics/CompleteLevel.png')
        self.image = pygame.transform.scale(spikes, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = spike_x
        self.rect.y = spike_y

    def update(self):
        # moves the level complete with the tilemap
        if player.speed == 0:
            self.rect.x -= 0
        if player.speed != 0:
            self.rect.x -= player.speed


# puts the tile map objects into groups
# one group is for level 1 and one group is for level 2
ground_enemy_group = pygame.sprite.Group()
roof_enemy_group = pygame.sprite.Group()
ground_enemy_group_2 = pygame.sprite.Group()
roof_enemy_group_2 = pygame.sprite.Group()
complete_level_group = pygame.sprite.Group()
complete_level_group_2 = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
spike_group_2 = pygame.sprite.Group()


# sets up the tile map to make the world
class World:
    def __init__(self, data):

        self.tile_list = []

        # tile map images
        main_floor = pygame.image.load('Graphics/FloorMain.png')
        right_side = pygame.image.load('Graphics/SideLeft.png')
        left_side = pygame.image.load('Graphics/SideRight.png')
        main_roof = pygame.image.load('Graphics/BottomMiddle.png')
        inside_bottom_right = pygame.image.load('Graphics/InsideBottomRight.png')
        inside_bottom_left = pygame.image.load('Graphics/InsideBottomLeft.png')
        inside_top_right = pygame.image.load('Graphics/InsideTopRight.png')
        inside_top_left = pygame.image.load('Graphics/InsideTopLeft.png')
        outside_top_left = pygame.image.load('Graphics/CornerLeft.png')
        outside_top_right = pygame.image.load('Graphics/CornerRight.png')
        outside_bottom_left = pygame.image.load('Graphics/BottomLeft.png')
        outside_bottom_right = pygame.image.load('Graphics/BottomRight.png')
        plain = pygame.image.load('Graphics/Middle.png')

        # sets the numbers for each tile to be added to the list
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # tile numbers are based on their index in the whole tilemap, including tiles not used
                if tile == 1:
                    # places tilemap image based on the number in the level list
                    # gets tiles rect to be able to size correctly
                    # is repeated for each tile
                    image = main_floor
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    image = outside_top_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)   
                if tile == 6:
                    image = right_side
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile) 
                if tile == 7:
                    image = plain
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    image = left_side
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)  
                if tile == 9:
                    image = outside_top_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 12:
                    image = outside_bottom_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 13:
                    image = main_roof
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 14:
                    image = outside_bottom_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 24:
                    image = inside_top_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 25:
                    image = inside_top_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 30:
                    image = inside_bottom_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 31:
                    image = inside_bottom_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)

                # objects below are set up in classes and are here just so they can be placed within the levels easier
                if tile == 35:
                    # adds object to a group
                    spikes = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group.add(spikes)

                if tile == 36:
                    # adds object to a group
                    spikes = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group_2.add(spikes)

                if tile == 37:
                    # adds object to a group
                    ground_enemies = GroundEnemies(col_count * tile_size, row_count * tile_size)
                    ground_enemy_group.add(ground_enemies)

                if tile == 38:
                    # adds object to a group
                    roof_enemies = RoofEnemies(col_count * tile_size, row_count * tile_size)
                    roof_enemy_group.add(roof_enemies)

                if tile == 39:
                    # adds object to a group
                    ground_enemies = GroundEnemies(col_count * tile_size, row_count * tile_size)
                    ground_enemy_group_2.add(ground_enemies)

                if tile == 40:
                    # adds object to a group
                    roof_enemies = RoofEnemies(col_count * tile_size, row_count * tile_size)
                    roof_enemy_group_2.add(roof_enemies)

                if tile == 100:
                    # adds object to a group
                    level_complete = LevelComplete(col_count * tile_size, row_count * tile_size)
                    complete_level_group.add(level_complete)

                if tile == 101:
                    # adds object to a group
                    level_complete = LevelComplete(col_count * tile_size, row_count * tile_size)
                    complete_level_group_2.add(level_complete)

                col_count += 1  # adds one to the collum count after it has finished checking
            row_count += 1  # adds one to the row count after it has finished checking

    # draws the tiles onto the screen
    def draw(self):
        for tile in self.tile_list:
            # lets the tiles scroll to allow the level to go beyond the screen
            screen.blit(tile[0], tile[1])
            tile[1][0] -= player.speed


# defines the separate levels for easy referencing
level1 = World(world_data1)
level2 = World(world_data2)

# adds music
mixer.init()
mixer.music.load('Sound/BG_Music.mp3')  # plays background music
mixer.music.play(-1)  # loops the music forever

# sets run to True
run = True
# runs everything in the game
while run:

    # makes the background appear on the screen
    parallax_background()

    if level_1 is True:

        # draws the level onto the screen
        level1.draw()
        # makes current level 0
        current_level = 0

        # adds the hazards and allows them to run within the game
        spike_group.update()
        ground_enemy_group.update()
        roof_enemy_group.update()
        complete_level_group.update()

        # draws the hazards on the screen
        spike_group.draw(screen)
        ground_enemy_group.draw(screen)
        roof_enemy_group.draw(screen)
        complete_level_group.draw(screen)

    if level_2 is True:

        # draws the level onto the screen
        level2.draw()
        # makes current level 1
        current_level = 1

        # adds the hazards and allows them to run within the game
        spike_group_2.update()
        ground_enemy_group_2.update()
        roof_enemy_group_2.update()
        complete_level_group_2.update()

        # draws the hazards on the screen
        spike_group_2.draw(screen)
        ground_enemy_group_2.draw(screen)
        roof_enemy_group_2.draw(screen)
        complete_level_group_2.draw(screen)

    # when each level begins playing these things will happen:
    if playing_game is True:

        # displays the score on screen
        text_surface = my_font.render('Score: ' + str(score), False, (255, 255, 255))
        screen.blit(text_surface, [25, screen_height - 25])

        # allows the players to run within the game
        player_group.update()
        player_group.draw(screen)

        # allows the gravity change function to run within the game
        gravity_change()

        # allows the players bullets to run within the game
        bullet_group.update()
        bullet_group.draw(screen)


        if game_over is True:
            pygame.time.delay(500)
            run = False

    # draws the start menu to the screen
    if start_menu is True:
        draw_start_menu()

    # draws the level select menu to the screen if the start_menu is False
    if level_select and start_menu is False:
        draw_level_select()

    # draws the pause menu to the screen when the game is paused
    if game_paused is True and start_menu is False and level_select is False:
        draw_pause()

    # stops the player from moving
    if key[pygame.K_ESCAPE]:
        game_paused = True
        player_move = False
        player.y_velocity = 0

    # allows key to be used instead of typing out the whole thing
    key = pygame.key.get_pressed()
    # quits the game when run is false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    tile_speed = player.speed  # makes the levels scroll

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
