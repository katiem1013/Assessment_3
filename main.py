import pygame

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode(( screen_width, screen_height))
clock = pygame.time.Clock()  # clock to set the frame rate

run = True
while run:

    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if key[pygame.K_ESCAPE]:
            run = False

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
