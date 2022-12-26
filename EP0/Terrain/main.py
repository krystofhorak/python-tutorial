import pygame
import noise 

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 2
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_TITLE = 'Terrain Generation'
pygame.display.set_caption(SCREEN_TITLE)

# Noise Settings
NOISE_SCALE = 0.01
NOISE_OCTAVES = 6

# Colors
SNOW_COLOR = (240, 240, 240)
DARKER_MOUNTAIN_COLOR = (90, 90, 90)
MOUNTAIN_COLOR = (150, 150 ,150)
DARKER_GRASS_COLOR = (38, 110, 30)
GRASS_COLOR = (55, 148, 44)
SAND_COLOR = (197, 204, 100)
SHORE_WATER_COLOR = (22, 65, 122)
WATER_COLOR = (13, 41, 79)
DARKER_WATER_COLOR = (10, 32, 61)

# Color Function
def get_color_by_noise_value(noise_value):
    if noise_value < -0.15:
        return DARKER_WATER_COLOR
    if noise_value < 0:
        return WATER_COLOR
    if noise_value < 0.05:
        return SHORE_WATER_COLOR
    if noise_value < 0.1:
        return SAND_COLOR
    if noise_value < 0.2:
        return GRASS_COLOR
    if noise_value < 0.3:
        return DARKER_GRASS_COLOR
    if noise_value < 0.35:
        return MOUNTAIN_COLOR
    if noise_value < 0.4:
        return DARKER_MOUNTAIN_COLOR 
    
    return SNOW_COLOR

# Generating the Terrain
for y in range(SCREEN_HEIGHT // TILE_SIZE):
    for x in range(SCREEN_WIDTH // TILE_SIZE):
        n = noise.pnoise2(x * NOISE_SCALE, y * NOISE_SCALE, octaves = NOISE_OCTAVES)
        drawn_color = get_color_by_noise_value(n)
        pygame.draw.rect(SCREEN, drawn_color, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
