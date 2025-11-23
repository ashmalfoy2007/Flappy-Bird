import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window
WIDTH = 400
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)

# Bird
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipes
pipe_width = 70
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Score
score = 0

def draw_window(bird_y, pipes, score):
    WIN.fill(BLUE)
    
    # Draw bird
    pygame.draw.rect(WIN, RED, (bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT))
    
    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(WIN, GREEN, pipe["top"])
        pygame.draw.rect(WIN, GREEN, pipe["bottom"])
    
    # Draw score
    score_text = FONT.render(str(score), True, WHITE)
    WIN.blit(score_text, (WIDTH // 2, 20))
    
    pygame.display.update()

def generate_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT)
    return {"top": top_pipe, "bottom": bottom_pipe}

def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            return True
    return False

def main():
    global bird_y, bird_velocity, pipes, score

    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [generate_pipe()]
    score = 0
    frame_count = 0
    running = True

    while running:
        clock.tick(FPS)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
        
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)

        # Pipe movement
        for pipe in pipes:
            pipe["top"].x -= pipe_velocity
            pipe["bottom"].x -= pipe_velocity
        
        # Remove off-screen pipes
        if pipes[0]["top"].right < 0:
            pipes.pop(0)
            score += 1
        
        # Generate new pipes
        if pipes[-1]["top"].x < WIDTH - 200:
            pipes.append(generate_pipe())
        
        # Collision detection
        if check_collision(bird_rect, pipes):
            break
        
        draw_window(bird_y, pipes, score)
    
    game_over()

def game_over():
    over_text = FONT.render("Game Over!", True, WHITE)
    WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.wait(2000)
    main()

if _name_ == "_main_":
    main()
