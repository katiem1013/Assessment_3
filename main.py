import pygame
import time
from Levels import level1, level2, screen, screen_width, screen_height, spike_group

pygame.init()

# what level is being selected
start_menu = True
level_1 = False
level_2 = False

# game variables
game_paused = False

# slows down the animations
start_frame = time.time()
noi = 6
frames_per_second = 10


pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate
font = pygame.font.Font(None, 40)


# screen flipping variables
gravity = 1  # 1 has the player at the bottom, 2 has the player at the top

# player variables
bullet_speed = -5

# background image and rect
background = pygame.image.load('Graphics/Background.png').convert()
background_rect = background.get_rect()

# to avoid having to write the whole thing out each time a key is pressed
key = pygame.key.get_pressed()

# gravity change cool down time
cool_down_GC = 300

# adds the idle images to a list so it can cycle through them
idle_images = []
for x in range(6):
    idle_images.append(pygame.image.load('Graphics/Player/Idle' + str(x) + '.png'))

# adds the running images to a list so it can cycle through them
run_images = []
for x in range(6):
    run_images.append(pygame.image.load('Graphics/Player/Run' + str(x) + '.png'))

# adds the falling images to a list so it can cycle through them
falling_images = []
for x in range(3):
    falling_images.append(pygame.image.load('Graphics/Player/Falling' + str(x) + '.png'))


class Player(pygame.sprite.Sprite):
    global gravity

    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = idle_images[0]
        self.y_velocity = 5
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_health = 1000
        self.max_health = 1000
        self.health_ratio = self.max_health / 400
        self.last_shot = pygame.time.get_ticks()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0
        self.direction = False  # True is left, False is Right
        self.gravity_position = False  # True is the roof, False is the floor

    def update(self):

        # global variables
        global bullet_speed
        global key

        # setting speed and cool down rate
        speed = 0
        cool_down = 500  # milliseconds

        # making the health bar update
        self.health_bar()

        # setting the y position of the player to be the y velocity
        self.rect.y += self.y_velocity

        # movement inputs
        if key[pygame.K_LEFT] and self.rect.left > 0:
            speed -= 8
            self.direction = True
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            speed += 8
            self.direction = False

        time_now = pygame.time.get_ticks()

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 1 and key[pygame.K_w] and time_now - self.last_shot > cool_down and self.y_velocity == 0:
            bullet = Bullets(self.rect.centerx + 10, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 2 and key[pygame.K_w] and time_now - self.last_shot > cool_down and self.y_velocity == 0:
            bullet = Bullets(self.rect.centerx + 10, self.rect.bottom)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # changes the way the player is falling when the gravity is changed
        if gravity == 1:
            self.y_velocity += 1
            # if the velocity goes beyond 5 it will set it back to 5
            if self.y_velocity > 5:
                self.y_velocity = 5

        # changes the way the player is falling when the gravity is changed
        if gravity == 2:
            self.y_velocity += 1
            # if the velocity goes beyond -5 it will set it back to -5
            if self.y_velocity > -5:
                self.y_velocity = -5

        # checking for collision
        for tile in level1.tile_list:

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
                    self.y_velocity = tile[1].top - self.rect.bottom
                    self.y_velocity = 0

        # check for collision with lava
        if pygame.sprite.spritecollide(self, spike_group, False):
            self.get_damage(10)
            self.y_velocity = tile[1].top - self.rect.bottom
            self.y_velocity = 0

        self.rect.x += speed

        # idle animation when the player is not moving
        if self.y_velocity == 0 and speed == 0:
            self.value += 1
            if self.value >= len(idle_images):
                self.value = 0
            self.image = idle_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # running animation when the player is moving
        if self.y_velocity == 0 and speed != 0:
            self.value += 1
            if self.value >= len(run_images):
                self.value = 0

            self.image = run_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # falling animation
        if self.y_velocity != 0:
            self.value += 1
            if self.value >= len(falling_images):
                self.value = 0

            self.image = falling_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # changes the direction of the player sprite based on the way they are walking
        if self.direction is True:
            player.image = pygame.transform.flip(player.image, True, False)
        if self.gravity_position is True:
            player.image = pygame.transform.flip(player.image, False, True)

    def get_damage(self, amount):

        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.current_health

    def health_bar(self):
        pygame.draw.rect(screen, (255, 87, 51), (10, 10, self.current_health / self.health_ratio, 25))
        pygame.draw.rect(screen, (170, 40, 10), (10, 10, 400, 25), 4)


# puts the player in a group
player_group = pygame.sprite.Group()

player = Player(int(screen_width / 4), screen_height - 500)
player_group.add(player)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += bullet_speed
        if self.rect.bottom > screen_height:
            self.kill()
        if self.rect.top < 0:
            self.kill()


def gravity_change():
    # global variables
    global gravity
    global bullet_speed
    global key
    global cool_down_GC

    # gives switching gravity a cool down in order to stop it being spammed
    cool_down_GC += clock.get_time()
    if cool_down_GC > 300:
        cool_down_GC = 0

    # sets the gravity and changes the bullet speed
    # also sets the player variables on whether or not the player is falling
    # flips the player animations as well
    if key[pygame.K_DOWN] and gravity == 2 and cool_down_GC == 0:
        gravity = 1
        bullet_speed = -5
        player.gravity_position = False
        player.image = pygame.transform.flip(player.image, False, True)
        bullet_group.empty()

    # sets the gravity and changes the bullet speed
    # also sets the player variables on whether or not the player is falling
    # flips the player animations as well
    if key[pygame.K_UP] and gravity == 1 and cool_down_GC == 0:
        gravity = 2
        bullet_speed = 5
        player.gravity_position = True
        player.image = pygame.transform.flip(player.image, False, True)
        bullet_group.empty()


# puts the bullets in a group
bullet_group = pygame.sprite.Group()

# sets the cool down to 0
cool_down_GC = 0


def draw_pause():

    global start_menu
    global game_paused
    global run

    # resume game button
    resume_button = pygame.draw.rect(screen, (181, 80, 136), [830, 200, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 200, 260, 70], 5, 5)
    text = font.render('Resume', True, 'black')
    screen.blit(text, (900, 222))
    if resume_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        game_paused = False
    else:
        game_paused = True

    # main menu button
    menu_button = pygame.draw.rect(screen, (181, 80, 136), [830, 400, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 400, 260, 70], 5, 5)
    text = font.render('Main Menu', True, 'black')
    screen.blit(text, (885, 422))
    if menu_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        start_menu = True
    else:
        start_menu = False

    # exit game button
    exit_button = pygame.draw.rect(screen, (181, 80, 136), [830, 600, 260, 70], 0, 15)
    pygame.draw.rect(screen, (181, 80, 136), [830, 600, 260, 70], 5, 5)
    text = font.render('Exit', True, 'black')
    screen.blit(text, (930, 622))
    if exit_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        run = False
    else:
        run = True


def draw_menu():
    pygame.draw.rect(screen, 'black', [100, 100, 300, 300])


run = True
while run:

    # makes the background appear on the screen
    screen.blit(background, (0, 0))

    if start_menu:
        draw_menu()

    # pause menu
    if game_paused is True and start_menu is False:
        draw_pause()
    if key[pygame.K_ESCAPE]:
        game_paused = True



    #if level_1 is True:
        # draws the level onto the screen
        #level1.draw()
        # draws the spikes onto the screen
        #spike_group.draw(screen)

    #if level_2 is True:
        ## draws the level onto the screen
        #level2.draw()
        # draws the spikes onto the screen
        #spike_group.draw(screen)

    #if start_menu is False:

        # allows the players to run within the game
       # player_group.update()
        #player_group.draw(screen)

        # allows the gravity change function to run within the game
        #gravity_change()

        # allows the players bullets to run within the game
        #bullet_group.update()
        #bullet_group.draw(screen)


    if player.current_health <= 0:
        run = False

    # allows key to be used instead of typing out the whole thing
    key = pygame.key.get_pressed()
    # quits the game when run is false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
