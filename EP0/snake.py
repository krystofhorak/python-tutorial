import pygame
import random

pygame.init()

# General Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 20
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_TITLE = 'Snake'
pygame.display.set_caption(SCREEN_TITLE)
GAME_FPS = 15

# Colors
BACKGROUND_COLOR = (22, 22, 22)
SNAKE_COLOR = (0, 255, 0)
FRUIT_COLOR = (255, 0, 0)

# Food Position Generation
def generate_food_position(snake_body):
    pos = [0, 0] 
    pos[0] = random.randint(0, SCREEN_WIDTH // TILE_SIZE - 1)
    pos[1] = random.randint(0, SCREEN_HEIGHT // TILE_SIZE - 1)
    while pos in snake_body:
        pos = generate_food_position(snake_body)
    return pos

# Snake Class
class Snake:
    def __init__(self):
        self.direction = [1, 0]
        self.body = [[3, 0], [2, 0], [1, 0]]

    def update(self):
        new_head_position = self.body[0].copy()
        new_head_position[0] += self.direction[0]
        new_head_position[1] += self.direction[1]

        # Wrapping Functionality
        if new_head_position[0] > SCREEN_WIDTH // TILE_SIZE - 1:
            new_head_position[0] = 0
        elif new_head_position[0] < 0:
            new_head_position[0] = SCREEN_WIDTH // TILE_SIZE - 1
        if new_head_position[1] > SCREEN_HEIGHT // TILE_SIZE - 1:
            new_head_position[1] = 0
        elif new_head_position[1] < 0:
            new_head_position[1] = SCREEN_HEIGHT // TILE_SIZE - 1

        self.body.insert(0, new_head_position)
        self.body.pop()

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def check_fruit_collision(self, food):
        return [food.x, food.y] == self.body[0]

    def grow(self):
        self.body.append(self.body[0])

    def draw(self):
        for part in self.body:
            pygame.draw.rect(SCREEN, SNAKE_COLOR, pygame.Rect(part[0] * TILE_SIZE, part[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Fruit Class
class Fruit:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def respawn(self, snake_body):
        new_position = generate_food_position(snake_body)
        self.x = new_position[0]
        self.y = new_position[1]

    def draw(self):
        pygame.draw.rect(SCREEN, FRUIT_COLOR, pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

running = True
snake = Snake()
initial_fruit_position = generate_food_position(snake.body)
fruit = Fruit(initial_fruit_position[0], initial_fruit_position[1])
clock = pygame.time.Clock()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # WSAD Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w') and snake.direction[1] != 1:
                snake.direction = [0, -1]
            elif event.key == pygame.K_DOWN or event.key == ord('s') and snake.direction[1] != -1:
                snake.direction = [0, 1]
            elif event.key == pygame.K_LEFT or event.key == ord('a') and snake.direction[0] != 1:
                snake.direction = [-1, 0]
            elif event.key == pygame.K_RIGHT or event.key == ord('d') and snake.direction[0] != -1:
                snake.direction = [1, 0]

    SCREEN.fill(BACKGROUND_COLOR)
    clock.tick(GAME_FPS)
    snake.update()

    # Collision Detection
    if snake.check_self_collision():
        print('Game over!')
        running = False
    if snake.check_fruit_collision(fruit):
        fruit.respawn(snake.body)
        snake.grow()

    snake.draw()
    fruit.draw()
    pygame.display.flip()
