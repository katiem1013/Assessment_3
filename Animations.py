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
    
# adds the death images to a list so if can cycle through them
death_images = []
for x in range(3):
    death_images.append(pygame.image.load('Graphics/Player/Death' + str(x) + '.png'))

# UPSIDE DOWN PLAYER ANIMATIONS
# adds the upside down idle images to a list so it can cycle through them
USD_idle_images = []
for x in range(6):
    USD_idle_images.append(pygame.image.load('Graphics/Player/USD_Idle' + str(x) + '.png'))    
    
# adds the upside down running images to a list so it can cycle through them
USD_run_images = []
for x in range(6):
    USD_run_images.append(pygame.image.load('Graphics/Player/USD_Run' + str(x) + '.png'))

# adds the upside down falling images to a list so it can cycle through them
USD_falling_images = []
for x in range(3):
    USD_falling_images.append(pygame.image.load('Graphics/Player/USD_Falling' + str(x) + '.png'))
                       
# adds the upside down death images to a list so if can cycle through them
USD_death_images = []
for x in range(3):
    USD_death_images.append(pygame.image.load('Graphics/Player/USD_Death' + str(x) + '.png'))
    
# ENEMY ANIMATIONS
# adds the idle images to a list so it can cycle through them
enemy_idle_images = []
for x in range(4):
    enemy_idle_images.append(pygame.image.load('Graphics/Enemy_One/Idle' + str(x) + '.png'))

# adds the running images to a list so it can cycle through them
enemy_run_images = []
for x in range(8):
    enemy_run_images.append(pygame.image.load('Graphics/Enemy_One/Run' + str(x) + '.png'))

# adds the running images to a list so it can cycle through them
roof_enemy_run_images = []
for x in range(8):
    roof_enemy_run_images.append(pygame.image.load('Graphics/Enemy_Two/Run' + str(x) + '.png'))

