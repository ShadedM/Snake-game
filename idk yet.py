import pygame
import time
import random
import json
import os

# Initialize pygame
pygame.init()

# Set up game screen dimensions for 720p resolution
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 102)
pink = (255, 105, 180)
purple = (128, 0, 128)

# Set up the clock for controlling the game speed
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 10
snake_speed = 15
border_thickness = 10  # Increased border thickness

# Font for displaying text
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 18)  # Smaller score font size

# Default controls
controls = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}

# File to save previous scores
score_file = "scores.json"

# Function to display the score
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, purple)  # Changed to purple color
    screen.blit(value, [0, 0])

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

# Function to display message
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3 + y_offset])

# Function to draw borders around the game screen
def draw_borders():
    # Draw thicker border
    pygame.draw.rect(screen, yellow, [0, 0, screen_width, screen_height], border_thickness)

# Function to generate food inside the borders with a 5% chance for a pink apple
def generate_food():
    foodx = round(random.randrange(border_thickness, screen_width - snake_block - border_thickness) / 10.0) * 10.0
    foody = round(random.randrange(border_thickness, screen_height - snake_block - border_thickness) / 10.0) * 10.0
    
    # 5% chance for a pink apple
    if random.random() < 0.05:
        food_color = pink
        food_value = 5  # Pink apple gives 5 score
    else:
        food_color = red
        food_value = 1  # Regular apple gives 1 score
    
    return foodx, foody, food_color, food_value

# Function to save score to file
def save_score(score):
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            scores = json.load(f)
    else:
        scores = []
    
    scores.append(score)
    with open(score_file, 'w') as f:
        json.dump(scores, f)

# Function to load previous scores from file
def load_scores():
    if os.path.exists(score_file):
        with open(score_file, 'r') as f:
            return json.load(f)
    return []

# Start screen with options and start button
def start_screen():
    start = False
    while not start:
        screen.fill(blue)
        message("Welcome to Snake Game!", yellow, -50)
        message("Press ENTER to Start", yellow, 0)
        message("Press O for Options", yellow, 40)
        message("Press P for Previous Scores", yellow, 80)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()  # Start the game
                if event.key == pygame.K_o:
                    options_menu()  # Open options menu
                if event.key == pygame.K_p:
                    previous_scores()  # Show previous scores

# Options menu to change controls and resolution
def options_menu():
    global controls, screen_width, screen_height
    setting = True
    while setting:
        screen.fill(blue)
        message("Options Menu", yellow, -50)
        message("Click on Control to Change", white, 0)
        
        # Draw control options as clickable areas
        up_text = font_style.render("Up: " + pygame.key.name(controls['up']), True, white)
        down_text = font_style.render("Down: " + pygame.key.name(controls['down']), True, white)
        left_text = font_style.render("Left: " + pygame.key.name(controls['left']), True, white)
        right_text = font_style.render("Right: " + pygame.key.name(controls['right']), True, white)

        screen.blit(up_text, (screen_width / 4, screen_height / 4))
        screen.blit(down_text, (screen_width / 4, screen_height / 4 + 40))
        screen.blit(left_text, (screen_width / 4, screen_height / 4 + 80))
        screen.blit(right_text, (screen_width / 4, screen_height / 4 + 120))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if the click is inside the "Up" button area
                if up_text.get_rect(topleft=(screen_width / 4, screen_height / 4)).collidepoint(mouse_pos):
                    controls['up'] = get_key_from_user()
                
                # Check if the click is inside the "Down" button area
                if down_text.get_rect(topleft=(screen_width / 4, screen_height / 4 + 40)).collidepoint(mouse_pos):
                    controls['down'] = get_key_from_user()

                # Check if the click is inside the "Left" button area
                if left_text.get_rect(topleft=(screen_width / 4, screen_height / 4 + 80)).collidepoint(mouse_pos):
                    controls['left'] = get_key_from_user()

                # Check if the click is inside the "Right" button area
                if right_text.get_rect(topleft=(screen_width / 4, screen_height / 4 + 120)).collidepoint(mouse_pos):
                    controls['right'] = get_key_from_user()

            # Check for key presses to change resolution
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    change_resolution()  # Change resolution
                if event.key == pygame.K_BACKSPACE:
                    start_screen()  # Return to start screen when backspace is pressed

# Function to get a key input from the user
def get_key_from_user():
    key_selected = None
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                key_selected = event.key
                waiting = False
    return key_selected

# Function to change screen resolution
def change_resolution():
    global screen_width, screen_height
    if screen_width == 1280:
        screen_width = 1920
        screen_height = 1080
    else:
        screen_width = 1280
        screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

# Function to show previous scores
def previous_scores():
    scores = load_scores()
    screen.fill(blue)
    message("Previous Scores", yellow, -50)
    if scores:
        for i, score in enumerate(scores[-5:], 1):  # Show last 5 scores
            message(f"{i}. {score}", white, 40 * i)
    else:
        message("No scores yet.", white, 40)

    pygame.display.update()

    # Wait for user to return to main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_screen()  # Return to main menu if Enter is pressed
                if event.key == pygame.K_BACKSPACE:
                    start_screen()  # Return to main menu if Backspace is pressed

# Main game loop function
def gameLoop():
    game_over = False
    game_close = False

    # Initial snake position
    x1 = screen_width / 2
    y1 = screen_height / 2

    # Snake movement direction
    x1_change = 0
    y1_change = 0

    # Snake body (initially empty)
    snake_List = []
    Length_of_snake = 1

    # Generate the first food inside the borders
    foodx, foody, food_color, food_value = generate_food()

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("You Lost! Press Q-Quit, C-Play Again or BACKSPACE for Main Menu", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            # Check for key presses to restart, quit, or return to the main menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_BACKSPACE:
                        start_screen()  # Return to main menu when Backspace is pressed

        # Handle key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == controls['left'] and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == controls['right'] and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == controls['up'] and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == controls['down'] and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check for game-over conditions (collision with boundaries)
        if x1 >= screen_width - snake_block - border_thickness or x1 < 0 + border_thickness or y1 >= screen_height - snake_block - border_thickness or y1 < 0 + border_thickness:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)

        # Draw the borders
        draw_borders()

        # Draw food and the snake
        pygame.draw.rect(screen, food_color, [foodx, foody, snake_block, snake_block])  # Draw food with color
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if snake collides with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if snake eats the food (collides with food)
        if x1 == foodx and y1 == foody:
            Length_of_snake += 1
            if food_value == 5:
                Length_of_snake += 4  # Increase the score more for pink apples
            foodx, foody, food_color, food_value = generate_food()  # Regenerate food inside the borders

        clock.tick(snake_speed)

    save_score(Length_of_snake - 1)
    pygame.quit()
    quit()

# Start the game
start_screen()
