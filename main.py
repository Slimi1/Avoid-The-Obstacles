import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Avoid the Obstacles")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up fonts
title_font = pygame.font.Font(None, 64)
menu_font = pygame.font.Font(None, 32)

# Set up the player character
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 6

# Set up the obstacle
obstacle_width = 100
obstacle_height = 20
obstacle_x = random.randint(0, window_width - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 5

# Set up start and quit rectangles
start_rect = pygame.Rect((window_width // 2 - 50, window_height // 2 + 50, 100, 40))
quit_rect = pygame.Rect((window_width // 2 - 50, window_height // 2 + 100, 100, 40))
# Set up game states
game_state = "menu"  # Possible states: "menu", "game", "game_over"

# Function to start the game
def start_game():
    global game_state
    game_state = "game"

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

# Function to draw the main menu
def draw_menu():
    window.fill(white)
    title_text = title_font.render("Avoid the Obstacles", True, black)
    start_text = menu_font.render("Start Game", True, black)
    quit_text = menu_font.render("Quit", True, black)

    title_rect = title_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
    start_rect = start_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
    quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

    window.blit(title_text, title_rect)
    window.blit(start_text, start_rect)
    window.blit(quit_text, quit_rect)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    start_game()
                elif quit_rect.collidepoint(mouse_pos):
                    quit_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
        player_x += player_speed

    window.fill(white)

    if game_state == "menu":
        draw_menu()

    elif game_state == "game":
        # Move the obstacle
        obstacle_y += obstacle_speed
        if obstacle_y > window_height:
            obstacle_x = random.randint(0, window_width - obstacle_width)
            obstacle_y = -obstacle_height

        # Check for collision
        if player_y < obstacle_y + obstacle_height and player_y + player_height > obstacle_y:
            if player_x < obstacle_x + obstacle_width and player_x + player_width > obstacle_x:
                # Collision occurred, game over
                game_state = "game_over"

        pygame.draw.rect(window, black, (player_x, player_y, player_width, player_height))
        pygame.draw.rect(window, black, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    elif game_state == "game_over":
        window.fill(white)
        game_over_text = title_font.render("Game Over", True, black)
        restart_text = menu_font.render("Restart", True, black)
        quit_text = menu_font.render("Quit", True, black)

        game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
        quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

        window.blit(game_over_text, game_over_rect)
        window.blit(restart_text, restart_rect)
        window.blit(quit_text, quit_rect)

        # Handle mouse click events in the game over screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos):
                game_state = "game"
                player_x = window_width // 2 - player_width // 2
                player_y = window_height - player_height - 10
                obstacle_x = random.randint(0, window_width - obstacle_width)
                obstacle_y = -obstacle_height
            elif quit_rect.collidepoint(mouse_pos):
                quit_game()

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
