import pygame
import sys

# Intialize PyGame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Physics
player_vel_y = 0
jump_speed = -25
gravity = 1
on_ground = False

# Colors
SKY = (135, 206, 250)
GROUND = (0, 0, 128)
CHECKPOINT = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNIV Final Project")

# Platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50),
    pygame.Rect(0, SCREEN_HEIGHT-270, SCREEN_WIDTH - 200, 50),
    pygame.Rect(200, SCREEN_HEIGHT-540, SCREEN_WIDTH - 200, 50)
]

# Checkpoints
checkpoints = [
    pygame.Rect(SCREEN_WIDTH - 70, SCREEN_HEIGHT - 90, 40, 40),
    pygame.Rect(20, 390, 40, 40),
    pygame.Rect(SCREEN_WIDTH - 70, 120, 40, 40)
]

tips = [
    ["If you're struggling in a class,",
     "go to office hours or the TA lab for the course!"],
    ["There are so many opportunities to serve others", 
     "on BYU campus! Stop by the Y-Serve office or get", 
     "involved in a service club that piques your interest!"],
    ["One of the coolest things about BYU is learning how to",
     "be a disciple-scholar. Make an effort to connect spirtual ",
     "and secular learning and notice how they overlap. And don't",
      " forget to pray for help in your classes!"]
]

completed_checkpoints = [False, False, False]

# Set the frame rate
clock = pygame.time.Clock()

# Player settings
cosmo = pygame.image.load("cosmo.png")
cosmo = pygame.transform.scale(cosmo, (int(cosmo.get_width() *0.2), cosmo.get_height() *0.2))
player_width = cosmo.get_width()
player_height = cosmo.get_height()
player_x = 0
player_y = SCREEN_HEIGHT - player_height -50
player_speed = 7

def show_tip(checkpoint_index):
    paused = True
    font = pygame.font.SysFont("calibri", 48)
    lines = tips[checkpoint_index]

    line_spacing = 10
    total_height = sum(font.size(line)[1] + line_spacing for line in lines) - line_spacing

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
        
        screen.fill(SKY)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 128))
        screen.blit(overlay, (0, 0))

        y_offset = SCREEN_HEIGHT//2 - total_height//2
        for line in lines:
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (SCREEN_WIDTH//2 - line_surface.get_width()//2, y_offset))
            y_offset += line_surface.get_height() + line_spacing

        pygame.display.flip()
        clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and on_ground:
        player_vel_y = jump_speed
        on_ground = False

    # Gravity
    player_vel_y += gravity
    player_y += player_vel_y

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    on_ground = False

    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_vel_y > 0 and player_rect.bottom - player_vel_y <= platform.top:
                player_y = platform.top - player_height
                player_vel_y = 0
                on_ground = True
            elif player_vel_y < 0 and player_rect.top - player_vel_y >= platform.top:
                player_y = platform.bottom
                player_vel_y = 0
        
    player_rect.topleft = (player_x, player_y)

    for i, cp in enumerate(checkpoints):
        if player_rect.colliderect(cp) and not completed_checkpoints[i]:
            completed_checkpoints[i] = True
            show_tip(i)

    # Fill the screen with a color (black in this case)
    screen.fill(SKY)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GROUND, platform)
    
    # Draw checkpoints
    for cp in checkpoints:
        pygame.draw.rect(screen, CHECKPOINT, cp)

    # Show the character
    screen.blit(cosmo, (player_x, player_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)
