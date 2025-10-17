import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mining Adventure")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
PURPLE = (200, 50, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 28)

# Player (spaceship)
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 80
player_vel_x = 5

# Resources (yellow normal, green rare)
resources = []

# Asteroids (hazards)
asteroids = []

# Missiles
missiles = []

# Power-ups
powerups = []

# Power-up timers
shield_timer = 0
double_score_timer = 0
rapid_fire_timer = 0

# Score & Level
score = 0
level = 1
spawn_timer = 0

# Background stars
bg_stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(60)]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Background stars
    for star in bg_stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), 2)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_vel_x
    if keys[pygame.K_SPACE]:
        missile_limit = 10 if rapid_fire_timer > 0 else 5
        if len(missiles) < missile_limit:
            missiles.append([player_x + player_width // 2, player_y])

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Increase difficulty
    spawn_timer += 1
    if spawn_timer > FPS * 10:  # every 10 seconds
        level += 1
        spawn_timer = 0

    # Generate resources
    while len(resources) < 5:
        x = random.randint(20, WIDTH - 20)
        y = random.randint(-300, -50)
        rare = random.random() < 0.2
        resources.append([x, y, rare])

    # Generate asteroids
    while len(asteroids) < 3 + level:
        x = random.randint(0, WIDTH - 20)
        y = random.randint(-300, -50)
        size = random.randint(15, 25)
        speed = random.uniform(2 + level*0.5, 4 + level*0.5)
        asteroids.append([x, y, size, speed])

    # Generate power-ups
    if random.random() < 0.002:  # low probability
        x = random.randint(20, WIDTH-20)
        y = random.randint(-300, -50)
        type_ = random.choice(["shield", "double_score", "rapid_fire"])
        powerups.append([x, y, type_])

    # Move resources
    for resource in resources:
        resource[1] += 2
        color = GREEN if resource[2] else YELLOW
        pygame.draw.circle(screen, color, (resource[0], resource[1]), 6)
        if player_rect.collidepoint(resource[0], resource[1]):
            points = 50 if not resource[2] else 150
            if double_score_timer > 0:
                points *= 2
            score += points
            resources.remove(resource)

    # Move asteroids
    for asteroid in asteroids:
        asteroid[1] += asteroid[3]
        pygame.draw.circle(screen, RED, (asteroid[0], asteroid[1]), asteroid[2])
        asteroid_rect = pygame.Rect(asteroid[0]-asteroid[2], asteroid[1]-asteroid[2], asteroid[2]*2, asteroid[2]*2)
        # Collision with player
        if player_rect.colliderect(asteroid_rect) and shield_timer <= 0:
            running = False
        # Collision with missiles
        for missile in missiles:
            if asteroid_rect.collidepoint(missile[0], missile[1]):
                try:
                    asteroids.remove(asteroid)
                    missiles.remove(missile)
                    score += 100
                except:
                    pass

    # Move missiles
    for missile in missiles:
        missile[1] -= 7
        pygame.draw.rect(screen, BLUE, (missile[0]-2, missile[1]-10, 4, 10))
    missiles = [m for m in missiles if m[1] > 0]

    # Move power-ups
    for pu in powerups:
        pu[1] += 2
        color = CYAN if pu[2]=="shield" else ORANGE if pu[2]=="double_score" else PURPLE
        pygame.draw.rect(screen, color, (pu[0]-5, pu[1]-5, 10, 10))
        if player_rect.collidepoint(pu[0], pu[1]):
            if pu[2] == "shield":
                shield_timer = FPS * 5  # 5 seconds
            elif pu[2] == "double_score":
                double_score_timer = FPS * 5
            elif pu[2] == "rapid_fire":
                rapid_fire_timer = FPS * 5
            powerups.remove(pu)

    powerups = [p for p in powerups if p[1] < HEIGHT + 10]

    # Decrease power-up timers
    if shield_timer > 0:
        shield_timer -= 1
    if double_score_timer > 0:
        double_score_timer -= 1
    if rapid_fire_timer > 0:
        rapid_fire_timer -= 1

    # Draw player (triangle spaceship)
    pygame.draw.polygon(screen, BLUE, [
        (player_x + player_width // 2, player_y),
        (player_x, player_y + player_height),
        (player_x + player_width, player_y + player_height)
    ])

    # Draw shield visual
    if shield_timer > 0:
        pygame.draw.circle(screen, CYAN, (player_x + player_width//2, player_y + player_height//2), 30, 2)

    # Draw score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(4000)

pygame.quit()
sys.exit()
