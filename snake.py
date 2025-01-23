import pygame
import time
import random
import math

# Initialize pygame
pygame.init()

# Display dimensions
width = 800
height = 600

# Create the display
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Beautiful Snake Game')

# Clock to control the speed of the game
clock = pygame.time.Clock()

# Snake block size and speed
block_size = 20
snake_speed = 15

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
background_color = (30, 30, 30)  # Dark gray
snake_color = (0, 255, 0)  # Green
food_color = (255, 0, 0)  # Red

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 40)
score_font = pygame.font.SysFont("comicsansms", 50)

# Cool background gradient
def draw_background():
    for y in range(height):
        # Gradient from dark gray to black
        color = (30 + int(20 * (y / height)), 30 + int(20 * (y / height)), 30 + int(20 * (y / height)))
        pygame.draw.line(game_window, color, (0, y), (width, y))

# Function to display the score
def display_score(score):
    score_text = score_font.render(f"Score: {score}", True, white)
    game_window.blit(score_text, [10, 10])

# Function to draw the snake
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(game_window, snake_color, [block[0], block[1], block_size, block_size])

# Function to display messages
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [width / 2 - mesg.get_width() / 2, height / 2 - mesg.get_height() / 2])

# Main game loop
def game_loop():
    game_over = False
    game_close = False
    paused = False

    # Initial position of the snake
    x = width / 2
    y = height / 2

    # Change in position
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:
        while game_close:
            draw_background()
            display_message("You Lost! Press Q-Quit or C-Play Again", red)
            display_score(snake_length - 1)
            pygame.display.update()

            # Check for player input after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block_size
                    x_change = 0
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            draw_background()
            display_message("Paused", white)
            pygame.display.update()
            continue

        # Wrap the snake around the edges
        if x >= width:
            x = 0
        elif x < 0:
            x = width - block_size
        if y >= height:
            y = 0
        elif y < 0:
            y = height - block_size

        # Update snake position
        x += x_change
        y += y_change
        draw_background()

        # Draw food
        pygame.draw.rect(game_window, food_color, [food_x, food_y, block_size, block_size])

        # Add new head to the snake
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Remove the tail if the snake is too long
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Draw the snake
        draw_snake(block_size, snake_list)
        display_score(snake_length - 1)

        # Update the display
        pygame.display.update()

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

        # Control the speed of the game
        clock.tick(snake_speed)

    # Quit pygame
    pygame.quit()
    quit()

# Start the game
game_loop()
