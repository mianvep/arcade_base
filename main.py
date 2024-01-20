import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Initialize mixer
pygame.mixer.init()

# Set up display
#WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH, HEIGHT = 720, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("plataforma arcade")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Function to load and resize images
def load_and_resize_image(filename, size):
    image = pygame.image.load(filename)
    return pygame.transform.scale(image, size)

# Load assets
background_image = load_and_resize_image("background.jpg", (WIDTH, HEIGHT))
player_image = load_and_resize_image("mario.png", (64, 64))
player_rect = player_image.get_rect()
player_rect.topleft = (100, 100)  # Initial position

# Load platform image
platform_image = load_and_resize_image("brick.png", (64, 64))
coin_image = load_and_resize_image("coin.png", (32, 32))
crown_image = load_and_resize_image("crown.png", (32, 32))

# Set up game variables
current_level = 0
player_speed = 8
player_jump = -20
player_y_speed = 0
gravity = 1
on_ground = False

# Level data
levels = [
    [
        pygame.Rect(100, HEIGHT - 100, 64, 64),
        pygame.Rect(300, HEIGHT - 200, 64, 64),
        pygame.Rect(500, HEIGHT - 300, 64, 64),
        pygame.Rect(700, HEIGHT - 400, 64, 64),
    ],
    [
        pygame.Rect(100, HEIGHT - 100, 64, 64),
        pygame.Rect(300, HEIGHT - 200, 64, 64),
        pygame.Rect(500, HEIGHT - 300, 64, 64),
        pygame.Rect(700, HEIGHT - 400, 64, 64),
        pygame.Rect(900, HEIGHT - 500, 64, 64),
        pygame.Rect(1100, HEIGHT - 400, 64, 64),
        pygame.Rect(1300, HEIGHT - 300, 64, 64),
    ]
]

# Invisible barrier to detect falling
bottom_barrier = pygame.Rect(0, HEIGHT - 1, WIDTH, 1)

# Game over variables
game_over = False
you_won = False

# Load sounds
jump_sound = pygame.mixer.Sound("jump_sound.wav")
die_sound = pygame.mixer.Sound("die_sound.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Player movement
    if not (game_over or you_won):  # Allow movement only if not game over or won
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_d] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # Jumping
        if keys[pygame.K_SPACE] and on_ground:
            player_y_speed = player_jump
            on_ground = False
            jump_sound.play()  # Play jump sound

    # Apply gravity to the player
    player_y_speed += gravity
    player_rect.y += player_y_speed

    # Check collision with the ground
    if player_rect.y > HEIGHT - player_rect.height:
        player_rect.y = HEIGHT - player_rect.height
        on_ground = True

    # Check collision with platforms
    for platform_rect in levels[current_level]:
        if player_rect.colliderect(platform_rect) and player_y_speed > 0 and player_rect.bottom > platform_rect.top:
            player_rect.y = platform_rect.y - player_rect.height
            on_ground = True
            player_y_speed = 0

    # Check for falling below the screen
    if player_rect.colliderect(bottom_barrier):
        game_over = True
        die_sound.play()  # Play die sound

    # Check for collecting the coin
    if not game_over and current_level == 0:
        coin_rect = pygame.Rect(700, HEIGHT - 450, 32, 32)
        if player_rect.colliderect(coin_rect):
            current_level += 1  # Move to the next level
            game_over = False
            you_won = False
            player_rect.x = levels[current_level][0].x  # Start on the first brick of the new level

    # Check for collecting the crown
    elif not game_over and current_level == 1:
        crown_rect = pygame.Rect(1300, HEIGHT - 350, 32, 32)
        if player_rect.colliderect(crown_rect):
            you_won = True
            win_sound.play()  # Play win sound

    # Update display
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # Draw player
    screen.blit(player_image, player_rect)

    # Draw platforms for the current level
    for platform_rect in levels[current_level]:
        screen.blit(platform_image, (platform_rect.x, platform_rect.y))

    # Draw coin in level 1
    if current_level == 0:
        screen.blit(coin_image, (700, HEIGHT - 450))

    # Draw crown in level 2
    elif current_level == 1:
        screen.blit(crown_image, (1300, HEIGHT - 350))

    # Draw game over or you won text
    if game_over:
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over! Press Esc to Quit", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    elif you_won:
        font = pygame.font.Font(None, 36)
        you_won_text = font.render("You Won! Thanks for Playing. Press Esc to Quit", True, RED)
        screen.blit(you_won_text, (WIDTH // 2 - you_won_text.get_width() // 2, HEIGHT // 2 - you_won_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Check for game over or you won and exit
    if game_over or you_won:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # Set frames per second
    clock.tick(60)
