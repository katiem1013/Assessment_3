import time
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
current_level = 0 # 0 is level 1, 1 is level 2

# slows down the animations
start_frame = time.time()
noi = 6
frames_per_second = 10

# screen variables
pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate
font = pygame.font.Font(None, 40)
background_scroll = 0  # controls the parallax background
left_edge = False  # determines when the end of the levels have been reached

# screen flipping variables
gravity = 1  # 1 has the player at the bottom, 2 has the player at the top
cool_down_GC = 300  # gravity change cool down time

# player variables
bullet_speed = -5
key = pygame.key.get_pressed()  # to avoid having to write the whole thing out each time a key is pressed


def parallax_background():
    for repeat in range(5):  # makes sure the background will repeat when it ends
        scroll_speed = 1
        for image in background_images:
            screen.blit(image, ((repeat * background_width) - background_scroll * scroll_speed, 0))


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
        self.health_ratio = self.max_health / 400
        self.last_shot = pygame.time.get_ticks()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0
        self.direction = False  # True is left, False is Right
        self.gravity_position = False  # True is the roof, False is the floor
        self.speed = 0

    def update(self):

        # global variables
        global bullet_speed
        global key
        global player_move
        global background_scroll

        # setting speed and cool down rate
        speed = 0
        cool_down = 500  # milliseconds

        # making the health bar update
        self.health_bar()

        # setting the y position of the player to be the y velocity
        self.rect.y += self.y_velocity

        # movement inputs
        if key[pygame.K_a] and self.rect.left > 0 and player_move is True and background_scroll > 0:
            speed -= 4
            background_scroll += -1
            self.direction = True
        if key[pygame.K_d] and self.rect.right < screen_width and player_move is True and background_scroll < 3000:
            speed += 4
            background_scroll += 1
            self.direction = False

        time_now = pygame.time.get_ticks()

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 1 and key[pygame.K_SPACE] and time_now - self.last_shot > cool_down and self.y_velocity == 0\
                and player_move is True:
            bullet = Bullets(self.rect.centerx + 10, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # changes the way the bullets shoot when the gravity is changed
        if gravity == 2 and key[pygame.K_SPACE] and time_now - self.last_shot > cool_down and self.y_velocity == 0\
                and player_move is True:
            bullet = Bullets(self.rect.centerx + 10, self.rect.bottom)
            bullet_group.add(bullet)
            self.last_shot = time_now

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
                        self.y_velocity = tile[1].top - self.rect.bottom
                        self.y_velocity = 0

        # check for collision with spikes
        if pygame.sprite.spritecollide(self, spike_group, False) and player_move is True:
            self.get_damage(10)
            self.y_velocity = tile[1].top - self.rect.bottom
            self.y_velocity = 0

        self.rect.x += speed

        # idle animation when the player is not moving
        if self.y_velocity == 0 and speed == 0 and player_move is True:
            self.value += 1
            if self.value >= len(idle_images):
                self.value = 0
            self.image = idle_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # running animation when the player is moving
        if self.y_velocity == 0 and speed != 0 and player_move is True:
            self.value += 1
            if self.value >= len(run_images):
                self.value = 0

            self.image = run_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # falling animation
        if self.y_velocity != 0 and player_move is True:
            self.value += 1
            if self.value >= len(falling_images):
                self.value = 0

            self.image = falling_images[self.value]
            self.value = int((time.time() - start_frame) * frames_per_second % noi)

        # changes the direction of the player sprite based on the way they are walking
        if self.direction is True and player_move is True:
            player.image = pygame.transform.flip(player.image, True, False)
        if self.gravity_position is True:
            player.image = pygame.transform.flip(player.image, False, True)

        # checks if the players health goes over the max amount of damage
        if self.current_health >= self.max_health:
            self.current_health = self.current_health

        if self.rect.bottom >= screen_height or self.rect.top <= 0:
            self.current_health -= 50

        self.speed = speed

        # update scroll based on player position
        if (self.rect.right > screen_width - 64 and background_scroll < (500 * tile_size) - screen_width) \
                or (self.rect.left < 64 and background_scroll > abs(self.speed)):
            self.rect.x -= self.speed

    def get_damage(self, amount):

        if self.current_health > 0 and player_move is True:
            self.current_health -= amount
        if self.current_health <= 0 and player_move is True:
            self.current_health = 0

    def health_bar(self):
        pygame.draw.rect(screen, (255, 87, 51), (10, 10, self.current_health / self.health_ratio, 35))
        pygame.draw.rect(screen, (170, 40, 10), (10, 10, 400, 35), 4)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, bullet_x, bullet_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = [bullet_x, bullet_y]

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

    global game_paused
    global start_menu
    global run
    global playing_game
    global level_1
    global level_2
    global player_move

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

    for pause in pygame.event.get():
        if pause.type == pygame.MOUSEBUTTONDOWN:
            if pause.button == 1:

                if resume_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    game_paused = False
                    playing_game = True
                    player_move = True

                if exit_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    run = False
                else:
                    run = True


def draw_start_menu():

    global game_paused
    global start_menu
    global level_select
    global level_1
    global run

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

    for start in pygame.event.get():
        if start.type == pygame.MOUSEBUTTONDOWN:
            if start.button == 1:

                if start_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    pygame.time.delay(500)
                    level_select = True
                    start_menu = False
                    game_paused = False

                if exit_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    run = False
                else:
                    run = True


def draw_level_select():

    global level_1
    global level_2
    global start_menu
    global level_select
    global playing_game
    global player_move

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

    for select in pygame.event.get():
        if select.type == pygame.MOUSEBUTTONDOWN:
            if select.button == 1:

                if level1_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    level_1 = True
                    level_select = False
                    playing_game = True
                    player_move = True
                    start_menu = False
                    player.rect.x = 64
                    player.rect.y = screen_height - 200
                    player.current_health = player.max_health

                if level2_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    level_2 = True
                    level_select = False
                    playing_game = True
                    player_move = True
                    start_menu = False
                    player.rect.x = 64
                    player.rect.y = screen_height - 200
                    player.current_health = player.max_health

                if back_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    start_menu = True
                    level_select = False


# puts the player in a group
player_group = pygame.sprite.Group()
player = Player(int(screen_width / 4), screen_height - 500)
player_group.add(player)

# puts the bullets in a group
bullet_group = pygame.sprite.Group()

# puts the tile map objects into groups
spike_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
ground_enemy_group = pygame.sprite.Group()


class GroundEnemies(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_idle_images[0]
        self.rect = self.image.get_rect()
        self.y_velocity = 5
        self.rect.x = player_x
        self.rect.y = player_y
        self.current_health = 50
        self.max_health = 50
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.value = 0
        self.move_counter = 0
        self.move_direction = 1

    def update(self):

        self.rect.x += self.move_direction
        self.move_counter -= 1
        if abs(self.move_counter) > 150:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

        if player.speed == 0:
            self.rect.x -= 0
        if player.speed != 0 and left_edge is False:
            self.rect.x -= player.speed

        self.rect.y += self.y_velocity

        if player_move is True:
            self.y_velocity += 1
            # if the velocity goes beyond 5 it will set it back to 5
            if self.y_velocity > 5:
                self.y_velocity = 5

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

        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.current_health -= 10
            bullet_group.remove()

        if self.current_health <= 0:
            self.kill()


# stops the screen scrolling once the player has reached the end of the level
class EndOfLevel(pygame.sprite.Sprite):
    def __init__(self, end_x, end_y):
        pygame.sprite.Sprite.__init__(self)
        end = pygame.image.load('Graphics/SideLeft.png')
        self.image = pygame.transform.scale(end, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = end_x
        self.rect.y = end_y

    def update(self):
        global left_edge
        if self.rect.x == screen_width - 64:
            left_edge = True
        else:
            left_edge = False

        if left_edge is False:
            self.rect.x -= player.speed
        if left_edge is True:
            self.rect.x -= 0


# spikes that will deal damage to the player when stood on
class Spike(pygame.sprite.Sprite):
    def __init__(self, spike_x, spike_y):
        pygame.sprite.Sprite.__init__(self)
        spikes = pygame.image.load('Graphics/Spike.png')
        self.image = pygame.transform.scale(spikes, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = spike_x
        self.rect.y = spike_y

    def update(self):

        if player.speed == 0:
            self.rect.x -= 0
        if player.speed != 0 and left_edge is False:
            self.rect.x -= player.speed


# sets up the tile map to make the world
class World:
    def __init__(self, data):

        global left_edge
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

        # sets the numbers for each tile to be added to the list
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    image = main_floor
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    image = left_side
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    image = right_side
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    image = main_roof
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    image = inside_bottom_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    image = inside_bottom_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    image = inside_top_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    image = inside_top_left
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
                if tile == 10:
                    image = outside_top_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 11:
                    image = outside_bottom_left
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                if tile == 12:
                    image = outside_bottom_right
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)

                if tile == 13:
                    spikes = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group.add(spikes)

                if tile == 14:
                    end = EndOfLevel(col_count * tile_size, row_count * tile_size)
                    end_group.add(end)

                if tile == 20:
                    ground_enemies = GroundEnemies(col_count * tile_size, row_count * tile_size)
                    ground_enemy_group.add(ground_enemies)

                col_count += 1
            row_count += 1

    def draw(self):
        global left_edge
        for tile in self.tile_list:
            if left_edge is False:
                tile[1][0] -= player.speed
            if left_edge is True:
                tile[1][0] -= 0

            screen.blit(tile[0], tile[1])


# defines the separate levels for easy referencing
level1 = World(world_data1)
level2 = World(world_data2)

run = True
while run:

    # makes the background appear on the screen
    parallax_background()

    if level_1 is True:
        # draws the level onto the screen
        level1.draw()
        # draws the spikes onto the screen
        spike_group.draw(screen)
        end_group.draw(screen)
        ground_enemy_group.draw(screen)


        current_level = 0

    if level_2 is True:
        # draws the level onto the screen
        level2.draw()
        # draws the spikes onto the screen
        spike_group.draw(screen)
        end_group.draw(screen)
        current_level = 1

    if playing_game is True:

        # allows the players to run within the game
        player_group.update()
        player_group.draw(screen)

        # allows the gravity change function to run within the game
        gravity_change()

        # allows the players bullets to run within the game
        bullet_group.update()
        bullet_group.draw(screen)

        spike_group.update()
        end_group.update()
        ground_enemy_group.update()

    # start menu
    if start_menu is True:
        draw_start_menu()

    if level_select and start_menu is False:
        draw_level_select()

    # pause menu
    if game_paused is True and start_menu is False and level_select is False:
        draw_pause()

    if key[pygame.K_ESCAPE]:
        game_paused = True
        player_move = False
        player.y_velocity = 0

    if player.current_health <= 0:
        run = False

    # allows key to be used instead of typing out the whole thing
    key = pygame.key.get_pressed()
    # quits the game when run is false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    tile_speed = player.speed

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
