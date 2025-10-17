import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mining Adventure")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load images with full paths
player_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Spaceship.png")
missile_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Missile.png")
asteroid_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Asteroid.png")
yellow_resource_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Yellow resource.png")
green_resource_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Green resource.png")
shield_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Shield Power-Up.png")
double_score_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Double Score.png")
rapid_fire_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Rapid Fire.png")
background_img = pygame.image.load(r"C:\Users\SATHVIKA\Downloads\jpg2png\Background.png")

# Resize images
player_img = pygame.transform.scale(player_img, (50, 40))
missile_img = pygame.transform.scale(missile_img, (6, 15))
asteroid_img = pygame.transform.scale(asteroid_img, (25, 25))
yellow_resource_img = pygame.transform.scale(yellow_resource_img, (12, 12))
green_resource_img = pygame.transform.scale(green_resource_img, (12, 12))
shield_img = pygame.transform.scale(shield_img, (20, 20))
double_score_img = pygame.transform.scale(double_score_img, (20, 20))
rapid_fire_img = pygame.transform.scale(rapid_fire_img, (20, 20))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Player setup
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_vel_x = 5

# Missile setup
missiles = []
missile_speed = 7

# Asteroid setup
asteroids = []
asteroid_speed = 3
asteroid_spawn_delay = 30
asteroid_timer = 0

# Resource setup
resources = []
resource_speed = 3
resource_spawn_delay = 60
resource_timer = 0

# Power-ups setup
powerups = []
powerup_speed = 2
powerup_spawn_delay = 600
powerup_timer = 0

# Score
score = 0
double_score_active = False
double_score_timer = 0

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.blit(background_img, (0, 0))  # Draw background

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fire missile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                missiles.append([player_x + player_width // 2, player_y])

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_vel_x

    # Update missiles
    for m in missiles[:]:
        m[1] -= missile_speed
        screen.blit(missile_img, (m[0]-3, m[1]-15))
        if m[1] < 0:
            missiles.remove(m)

    # Spawn asteroids
    asteroid_timer += 1
    if asteroid_timer >= asteroid_spawn_delay:
        asteroid_timer = 0
        asteroids.append([random.randint(0, WIDTH-25), -25])

    # Update asteroids
    for a in asteroids[:]:
        a[1] += asteroid_speed
        screen.blit(asteroid_img, (a[0], a[1]))
        if a[1] > HEIGHT:
            asteroids.remove(a)

        # Collision with missile
        for m in missiles[:]:
            if pygame.Rect(a[0], a[1], 25, 25).colliderect(pygame.Rect(m[0]-3, m[1]-15, 6, 15)):
                asteroids.remove(a)
                missiles.remove(m)
                score += 2 if double_score_active else 1
                break

    # Spawn resources
    resource_timer += 1
    if resource_timer >= resource_spawn_delay:
        resource_timer = 0
        resource_type = random.choice(["yellow", "green"])
        resources.append([random.randint(0, WIDTH-12), -12, resource_type])

    # Update resources
    for r in resources[:]:
        r[1] += resource_speed
        img = yellow_resource_img if r[2]=="yellow" else green_resource_img
        screen.blit(img, (r[0], r[1]))
        if r[1] > HEIGHT:
            resources.remove(r)
        # Collision with player
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(pygame.Rect(r[0], r[1], 12, 12)):
            score += 5 if r[2]=="yellow" else 10
            resources.remove(r)

    # Spawn power-ups
    powerup_timer += 1
    if powerup_timer >= powerup_spawn_delay:
        powerup_timer = 0
        ptype = random.choice(["shield", "double", "rapid"])
        powerups.append([random.randint(0, WIDTH-20), -20, ptype])

    # Update power-ups
    for pu in powerups[:]:
        pu[1] += powerup_speed
        if pu[2]=="shield":
            screen.blit(shield_img, (pu[0], pu[1]))
        elif pu[2]=="double":
            screen.blit(double_score_img, (pu[0], pu[1]))
        elif pu[2]=="rapid":
            screen.blit(rapid_fire_img, (pu[0], pu[1]))
        # Collision with player
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(pygame.Rect(pu[0], pu[1], 20, 20)):
            if pu[2]=="double":
                double_score_active = True
                double_score_timer = 600  # lasts 10 seconds at 60 FPS
            powerups.remove(pu)

    # Update double score timer
    if double_score_active:
        double_score_timer -= 1
        if double_score_timer <= 0:
            double_score_active = False

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
