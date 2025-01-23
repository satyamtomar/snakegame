from js import document, window
import math
import random

# Get the canvas and context
canvas = document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")

# Game settings
grid_size = 20
tile_count = canvas.width // grid_size

# Snake and food
snake = [{"x": 10, "y": 10}]
food = {"x": 5, "y": 5}
direction = {"x": 0, "y": 0}
score = 0

# Function to draw the game
def draw():
    # Clear the canvas
    ctx.fillStyle = "#1a1a1a"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    # Draw the snake
    ctx.fillStyle = "lime"
    for segment in snake:
        ctx.fillRect(segment["x"] * grid_size, segment["y"] * grid_size, grid_size, grid_size)

    # Draw the food
    ctx.fillStyle = "red"
    ctx.fillRect(food["x"] * grid_size, food["y"] * grid_size, grid_size, grid_size)

    # Draw the score
    ctx.fillStyle = "white"
    ctx.font = "20px Arial"
    ctx.fillText(f"Score: {score}", 10, 30)

# Function to update the game state
def update():
    global score

    # Move the snake
    head = {"x": snake[0]["x"] + direction["x"], "y": snake[0]["y"] + direction["y"]}

    # Wrap around the edges
    if head["x"] < 0:
        head["x"] = tile_count - 1
    if head["x"] >= tile_count:
        head["x"] = 0
    if head["y"] < 0:
        head["y"] = tile_count - 1
    if head["y"] >= tile_count:
        head["y"] = 0

    # Check for collisions with itself
    for segment in snake:
        if segment["x"] == head["x"] and segment["y"] == head["y"]:
            reset_game()
            return

    snake.insert(0, head)

    # Check if snake eats food
    if head["x"] == food["x"] and head["y"] == food["y"]:
        score += 1
        place_food()
    else:
        snake.pop()

# Function to place food randomly
def place_food():
    food["x"] = random.randint(0, tile_count - 1)
    food["y"] = random.randint(0, tile_count - 1)

    # Ensure food doesn't spawn on the snake
    for segment in snake:
        if segment["x"] == food["x"] and segment["y"] == food["y"]:
            place_food()
            break

# Function to reset the game
def reset_game():
    global snake, direction, score
    snake = [{"x": 10, "y": 10}]
    direction = {"x": 0, "y": 0}
    score = 0
    place_food()

# Handle keyboard input
def on_keydown(event):
    if event.key == "ArrowUp" and direction["y"] == 0:
        direction["x"] = 0
        direction["y"] = -1
    elif event.key == "ArrowDown" and direction["y"] == 0:
        direction["x"] = 0
        direction["y"] = 1
    elif event.key == "ArrowLeft" and direction["x"] == 0:
        direction["x"] = -1
        direction["y"] = 0
    elif event.key == "ArrowRight" and direction["x"] == 0:
        direction["x"] = 1
        direction["y"] = 0

# Add event listener for keyboard input
window.addEventListener("keydown", on_keydown)

# Game loop
def game_loop():
    update()
    draw()
    window.requestAnimationFrame(game_loop)

# Start the game
place_food()
game_loop()
