import pygame

# background images
background_images = []
for i in range(5):
    background = pygame.image.load(f'Graphics/Background{i}.png').convert_alpha()
    background_images.append(background)

background_width = background_images[0].get_width()

# PLAYER ANIMATIONS
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

# ENEMY ANIMATIONS
# adds the idle images to a list so it can cycle through them
enemy_idle_images = []
for x in range(4):
    enemy_idle_images.append(pygame.image.load('Graphics/Enemy_One/Idle' + str(x) + '.png'))

# adds the running images to a list so it can cycle through them
enemy_run_images = []
for x in range(8):
    enemy_run_images.append(pygame.image.load('Graphics/Enemy_One/Run' + str(x) + '.png'))
