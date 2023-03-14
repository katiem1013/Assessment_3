import pygame

pygame.init()

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Assessment 3')
clock = pygame.time.Clock()  # clock to set the frame rate

colour = 1  # 1 is Black, 2 is White
clicking = False

background_black = pygame.image.load('Graphics/BackgroundBlack.png').convert()
background_white = pygame.image.load('Graphics/BackgroundWhite.png').convert()

floor_black = pygame.image.load('Graphics/FloorBlack.png').convert()
floor_white = pygame.image.load('Graphics/FloorWhite.png').convert()

background_white_rect = background_white.get_rect()
background_black_rect = background_black.get_rect()

painting = []
active_colour = 229, 255, 204


def draw_painting(paints):
    for i in range(len(paints)):
        pygame.draw.circle(screen, paints[i][0], paints[i][1], paints[i][2])


class Player1(pygame.sprite.Sprite):
    global colour

    def __init__(self, x_pos2, y_pos2, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Graphics/Player.png')
        self.rect = self.image.get_rect()
        self.x_pos2 = x_pos2
        self.y_pos2 = y_pos2
        self.rect.center = [x_pos2, y_pos2]
        self.health_start = health
        self.health_remaining = health

    def update(self):
        speed = 8
        # movement inputs
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width/2:
            self.rect.x += speed
        if key[pygame.K_UP] and self.rect.bottom > 0:
            pass


class Player2:
    def __init__(self, x_pos2, y_pos2):
        self.x_pos2 = x_pos2
        self.y_pos2 = y_pos2


def colour_change():
    global colour
    global clicking
    key = pygame.key.get_pressed()
    if key[pygame.K_1] and colour == 2:
        colour = 1
        painting.clear()
    if key[pygame.K_2] and colour == 1:
        colour = 2
        painting.clear()
    if colour == 1:
        screen.blit(background_white, (0, 0))
        screen.blit(floor_black, (0, screen_height - 175))
        screen.blit(background_black, (screen_width / 2, 0))
        screen.blit(floor_white, (screen_width / 2, 0))
    if colour == 2:
        screen.blit(background_white, (0, 0))
        screen.blit(floor_black, (0, 0))
        screen.blit(background_black, (screen_width / 2, 0))
        screen.blit(floor_white, (screen_width / 2, screen_height - 175))

    location = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        pygame.draw.circle(screen, active_colour, location, 30)
        painting.append((active_colour, location, 30))

    draw_painting(painting)


player_group = pygame.sprite.Group()
player = Player1(int(screen_width / 4), screen_height - 207, 3)
player_group.add(player)

run = True
while run:

    colour_change()
    player_group.update()
    player_group.draw(screen)

    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if key[pygame.K_ESCAPE]:
            run = False

    pygame.draw.line(screen, (150, 200, 220), (screen_width/2, 0), (screen_width/2, screen_height), 5)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
