import pygame
pygame.init()

# screen variables
screen_width = 1920
screen_height = 1080

# screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate

# tile map
tile_size = 64

# screen flipping variables
colour = 1  # 1 has player 1s platform at the bottom, 2 has the platform at the top

# player variables
player_velocity = 5
bullet_speed = -5

# background colours
background_black = pygame.image.load('Graphics/BackgroundBlack.png').convert()
background_white = pygame.image.load('Graphics/BackgroundBlack.png').convert()

# background rects
background_white_rect = background_white.get_rect()
background_black_rect = background_black.get_rect()


class Player(pygame.sprite.Sprite):
    global colour
    global player_velocity

    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Player.png').convert()
        self.x = 0
        self.y = 0
        self.y_velocity = player_velocity
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        speed = 8
        y_collision = 0
        self.rect.y += self.y_velocity
        cooldown = 500  # milliseconds
        global bullet_speed
        key = pygame.key.get_pressed()
        # movement inputs
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if colour == 1 and key[pygame.K_w] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            bullet_speed = -5
            self.last_shot = time_now

        if colour == 2 and key[pygame.K_w] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.bottom)
            bullet_group.add(bullet)
            bullet_speed = 5
            self.last_shot = time_now

        # checking for collision
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                speed = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                # check if the player is hitting the ground or roof
                if self.y_velocity < 0:
                    y_collision = tile[1].bottom - self.rect.top
                if self.y_velocity >= 0:
                    y_collision = tile[1].top - self.rect.bottom

        self.rect.y += y_collision


class World():
    def __init__(self, data):
        self.tile_list = []

        main_floor = pygame.image.load('Graphics/FloorMain.png')
        right_side = pygame.image.load('Graphics/SideLeft.png')

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
                    image = right_side
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)




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
    global colour
    global bullet_speed
    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN] and colour == 2:
        colour = 1
        player.y_velocity = 5
        bullet_speed = -5

    if key[pygame.K_UP] and colour == 1:
        colour = 2
        player.y_velocity = -5
        bullet_speed = 5


player_group = pygame.sprite.Group()

player = Player(int(screen_width / 4), screen_height - 500)
player_group.add(player)

bullet_group = pygame.sprite.Group()

run = True
while run:

    # makes the backgrounds appear on the screen
    screen.blit(background_white, (0, 0))
    screen.blit(background_black, (screen_width / 2, 0))

    # allows the colour change function to run within the game
    gravity_change()

    world.draw()

    # allows the players to run within the game
    player_group.update()
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    # allows key to be used instead of typing out the whole thing
    key = pygame.key.get_pressed()
    # quits the game when run is false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # escape turns run to false
        if key[pygame.K_ESCAPE]:
            run = False

    # player collision with the floors, sets the players velocity to 0 so they stop falling
    #if player.rect.colliderect(floor_black):
    #    player.y_velocity = 0

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
