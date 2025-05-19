import pygame
import random

pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Block size
block_size = 20

# Game variables
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_x_change = 0
snake_y_change = 0
snake_list = []
snake_length = 1
game_over = False
game_paused = False
game_speed = 15  # Default speed
level = 1  # Default level


# Function to display the snake
def display_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, green, [x, y, block_size, block_size])


# Function to display the score
def display_score(score):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))


# Function to display the level
def display_level(level):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Level: " + str(level), True, blue)
    screen.blit(text, (10, 40))


# Function to display game over message
def display_game_over():
    font = pygame.font.SysFont(None, 60)
    text = font.render("GAME OVER", True, red)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)


# Function to display pause message
def display_pause():
    font = pygame.font.SysFont(None, 60)
    text = font.render("PAUSED", True, blue)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)


# Initialize food
food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
score = 0

clock = pygame.time.Clock()

# Main game loop
while True:
    while game_over:
        screen.fill(black)
        display_game_over()
        display_score(score)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    snake_x = screen_width / 2
                    snake_y = screen_height / 2
                    snake_x_change = 0
                    snake_y_change = 0
                    snake_list = []
                    snake_length = 1
                    game_over = False
                    score = 0
                    level = 1
                    game_speed = 15

    while game_paused:
        screen.fill(black)
        display_pause()
        display_score(score)
        display_level(level)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Unpause game
                    game_paused = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_x_change != block_size:
                snake_x_change = -block_size
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT and snake_x_change != -block_size:
                snake_x_change = block_size
                snake_y_change = 0
            elif event.key == pygame.K_UP and snake_y_change != block_size:
                snake_y_change = -block_size
                snake_x_change = 0
            elif event.key == pygame.K_DOWN and snake_y_change != -block_size:
                snake_y_change = block_size
                snake_x_change = 0
            if event.key == pygame.K_p:  # Pause game
                game_paused = True
            if event.key == pygame.K_l: #increase level
                level += 1
                game_speed += 5


    # Check for boundaries
    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
        game_over = True

    snake_x += snake_x_change
    snake_y += snake_y_change

    screen.fill(black)
    pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)

    if len(snake_list) > snake_length:
        del snake_list[0]

    # Check for self-collision
    for x in snake_list[:-1]:
        if x == snake_head:
            game_over = True

    display_snake(snake_list)
    display_score(score)
    display_level(level)
    pygame.display.update()

    # Check for food collision
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
        food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
        snake_length += 1
        score += 1

    clock.tick(game_speed)

pygame.quit()
quit()