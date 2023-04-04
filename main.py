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
gravity = 1  # 1 has the player at the bottom, 2 has the player at the top

# player variables
bullet_speed = -5

# background colours
background = pygame.image.load('Graphics/Background.png').convert()

# background rects
background_rect = background.get_rect()

key = pygame.key.get_pressed()


class Player(pygame.sprite.Sprite):
    global gravity

    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Player.png').convert()
        self.y_velocity = 5
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision = False

    def update(self):
        speed = 0
        self.rect.y += self.y_velocity
        cool_down = 500  # milliseconds
        global bullet_speed
        global key
        # movement inputs
        if key[pygame.K_LEFT] and self.rect.left > 0:
            speed -= 8
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            speed += 8

        time_now = pygame.time.get_ticks()

        if gravity == 1 and key[pygame.K_w] and time_now - self.last_shot > cool_down:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            bullet_speed = -5
            self.last_shot = time_now

        if gravity == 2 and key[pygame.K_w] and time_now - self.last_shot > cool_down:
            bullet = Bullets(self.rect.centerx, self.rect.bottom)
            bullet_group.add(bullet)
            bullet_speed = 5
            self.last_shot = time_now

        # checking for collision
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + speed, self.rect.y, self.width, self.height):
                self.collision = True
                speed = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                self.collision = True
                if self.y_velocity == 5:
                    self.y_velocity = tile[1].bottom - self.rect.top
                    self.y_velocity = 0
                # check if above the ground i.e. falling
                if self.y_velocity >= 0:
                    self.y_velocity = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.y_velocity, self.width, self.height):
                self.collision = True
                if self.y_velocity == -5:
                    self.y_velocity = 0
                # check if above the ground i.e. falling
                if self.y_velocity <= 0:
                    self.y_velocity = tile[1].top - self.rect.bottom
                    self.y_velocity = 0
            if tile[0].get_rect().colliderect(player):
                self.collision = False

        self.rect.x += speed


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

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_data = [
    [8, 4, 4, 7, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 10, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 5]
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
    global gravity
    global bullet_speed
    global key
    if key[pygame.K_DOWN] and gravity == 2:
        gravity = 1
        player.y_velocity = 5
        bullet_speed = -5
        player.image = pygame.transform.rotate(player.image, 180)

    if key[pygame.K_UP] and gravity == 1:
        gravity = 2
        player.y_velocity = -5
        bullet_speed = 5
        player.image = pygame.transform.rotate(player.image, 180)


player_group = pygame.sprite.Group()

player = Player(int(screen_width / 4), screen_height - 500)
player_group.add(player)

bullet_group = pygame.sprite.Group()

run = True
while run:

    # makes the background appear on the screen
    screen.blit(background, (0, 0))

    # allows the gravity change function to run within the game
    gravity_change()

    world.draw()

    # allows the players to run within the game
    player_group.update()
    player_group.draw(screen)

    print(player.collision)

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

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
