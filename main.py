import pygame
pygame.init()

screen_width = 1000
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
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


class Player1:
    def __init__(self, x_pos2, y_pos2):
        self.x_pos2 = x_pos2
        self.y_pos2 = y_pos2


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
    if colour == 2:
        screen.blit(background_black, (0, 0))
        screen.blit(floor_white, (0, screen_height - 175))

    location = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        pygame.draw.circle(screen, active_colour, location, 30)
        painting.append((active_colour, location, 30))

    draw_painting(painting)

run = True
while run:

    colour_change()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if key[pygame.K_ESCAPE]:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
