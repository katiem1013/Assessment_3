import pygame

# screen variables
screen_width = 1920
screen_height = 1080

# screen setup
screen = pygame.display.set_mode((screen_width, screen_height))

# tile map
tile_size = 64


# to avoid having to write the whole thing out each time a key is pressed
key = pygame.key.get_pressed()


# spikes that will deal damage to the player when stood on
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spikes = pygame.image.load('Graphics/Spike.png')
        self.image = pygame.transform.scale(spikes, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# sets up the tile map to make the world
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

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            tile[1][0] += player.speed
            screen.blit(tile[0], tile[1])


world_data1 = [
    [8, 4, 4, 7, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 8, 4, 4, 7],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 10, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [6, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 5]
]


world_data2 = [
    [8, 4, 4, 7, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 8, 4, 4, 7],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 12, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 10, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 3],
    [6, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 5]
]


spike_group = pygame.sprite.Group()

level1 = World(world_data1)
level2 = World(world_data2)
