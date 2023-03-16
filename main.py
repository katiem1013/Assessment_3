import pygame
pygame.init()

# screen variables
screen_width = 1920
screen_height = 1080

# screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate

# screen flipping variables
colour = 1  # 1 has player 1s platform at the bottom, 2 has the platform at the top

# player variables
player_1_velocity = 5
player_2_velocity = -5
speed = 8
bullet_speed_1 = -5
bullet_speed_2 = 5

# background colours
background_black = pygame.image.load('Graphics/BackgroundBlack.png').convert()
background_white = pygame.image.load('Graphics/BackgroundWhite.png').convert()

# floor locations for the black flooring
floor_black_location_y = 905
floor_black_location_x = 0

# floor locations for the white flooring
floor_white_location_y = 0
floor_white_location_x = 960

# background rects
background_white_rect = background_white.get_rect()
background_black_rect = background_black.get_rect()

# variables for drawing on the screen
painting = []
active_colour = 229, 255, 204
clicking = False


# fun little drawing feature, doesn't do anything gameplay wise
def draw_painting(paints):
    for i in range(len(paints)):
        pygame.draw.circle(screen, paints[i][0], paints[i][1], paints[i][2])


class Player1(pygame.sprite.Sprite):
    global colour
    global player_1_velocity

    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Player.png')
        self.x = 0
        self.y = 0
        self.y_velocity = player_1_velocity
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = 100
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.y_velocity
        cooldown = 300  # milliseconds

        # movement inputs
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screen_width/2:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if colour == 2 and key[pygame.K_w] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.bottom)
            bullet_group.add(bullet)
            self.last_shot = time_now
        if colour == 1 and key[pygame.K_w] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now


class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Player.png')
        self.x = 0
        self.y = 0
        self.y_velocity = player_2_velocity
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = 100
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.y_velocity
        cooldown = 300  # milliseconds

        # movement inputs
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > screen_width/2:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()

        if colour == 1 and key[pygame.K_UP] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
        if colour == 2 and key[pygame.K_UP] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.bottom)
            bullet_group.add(bullet)
            self.last_shot = time_now


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += bullet_speed_1
        self.rect.y += bullet_speed_2
        if self.rect.bottom < 0:
            self.kill()


def colour_change():
    # global variables
    global colour
    global clicking
    global floor_white_location_y
    global floor_black_location_y
    global bullet_speed_1
    global bullet_speed_2

    key = pygame.key.get_pressed()
    if key[pygame.K_COMMA] and colour == 2:
        colour = 1
        player.y_velocity = 5
        player2.y_velocity = -5
        painting.clear()
        bullet_speed_1 = -5
        bullet_speed_2 = 5
        floor_white_location_y = 0
        floor_black_location_y = 905

    if key[pygame.K_PERIOD] and colour == 1:
        colour = 2
        player.y_velocity = -5
        player2.y_velocity = 5
        painting.clear()
        bullet_speed_1 = 5
        bullet_speed_2 = -5
        floor_white_location_y = 905
        floor_black_location_y = 0

    location = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        pygame.draw.circle(screen, active_colour, location, 30)
        painting.append((active_colour, location, 30))

    draw_painting(painting)


player_group = pygame.sprite.Group()

player = Player1(int(screen_width / 4), screen_height - 500)
player2 = Player2(int(screen_width / 1.3), screen_height - 500)
player_group.add(player, player2)

bullet_group = pygame.sprite.Group()

run = True
while run:

    # makes the backgrounds appear on the screen
    screen.blit(background_white, (0, 0))
    screen.blit(background_black, (screen_width / 2, 0))

    # draws the ground instead of using an image to get them
    floor_white = pygame.draw.rect(screen, (217, 217, 217), (floor_white_location_x, floor_white_location_y, 960, 175), 100)
    floor_black = pygame.draw.rect(screen, (51, 51, 51), (floor_black_location_x, floor_black_location_y, 960, 175), 100)

    # allows the colour change function to run within the game
    colour_change()

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
    if player.rect.colliderect(floor_black):
        player.y_velocity = 0
    if player2.rect.colliderect(floor_white):
        player2.y_velocity = 0

    # draws the line separating the two players on the screen
    pygame.draw.line(screen, (150, 200, 220), ((screen_width/2) - 2.5, 0), ((screen_width/2) - 2.5, screen_height), 5)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
