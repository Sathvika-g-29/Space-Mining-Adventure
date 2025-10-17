import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌌 Space Mining Adventure")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 30)

# Paths to images 
image_paths = {
    "spaceship": r"C:\Users\SATHVIKA\Downloads\jpg2png\Spaceship.png",
    "yellow_resource": r"C:\Users\SATHVIKA\Downloads\jpg2png\Yellow resource.png",
    "green_resource": r"C:\Users\SATHVIKA\Downloads\jpg2png\Green resource.png",
    "asteroid": r"C:\Users\SATHVIKA\Downloads\jpg2png\Asteroid.png",
    "missile": r"C:\Users\SATHVIKA\Downloads\jpg2png\Missile.png",
    "shield": r"C:\Users\SATHVIKA\Downloads\jpg2png\Shield Power-Up.png",
    "double_score": r"C:\Users\SATHVIKA\Downloads\jpg2png\Double Score.png",
    "rapid_fire": r"C:\Users\SATHVIKA\Downloads\jpg2png\Rapid Fire.png"
}

# Load images
images = {key: pygame.image.load(path).convert_alpha() for key, path in image_paths.items()}

# Resize images
images["spaceship"] = pygame.transform.scale(images["spaceship"], (90, 75))
images["yellow_resource"] = pygame.transform.scale(images["yellow_resource"], (30, 30))
images["green_resource"] = pygame.transform.scale(images["green_resource"], (30, 30))
images["asteroid"] = pygame.transform.scale(images["asteroid"], (60, 60))
images["missile"] = pygame.transform.scale(images["missile"], (15, 35))
images["shield"] = pygame.transform.scale(images["shield"], (45, 45))
images["double_score"] = pygame.transform.scale(images["double_score"], (40, 40))
images["rapid_fire"] = pygame.transform.scale(images["rapid_fire"], (40, 40))

# Player setup
player_width, player_height = 90, 75
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_vel_x = 5

# Game elements
resources = []
asteroids = []
missiles = []
powerups = []

# Power-up timers
shield_timer = 0
double_score_timer = 0
rapid_fire_timer = 0

# Score & Level
score = 0
level = 1
spawn_timer = 0
asteroid_spawn_timer = 0

# Background stars
bg_stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(60)]

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Background

    # Draw background stars
    for star in bg_stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 2)

    # Event handling
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
        missile_limit = 8 if rapid_fire_timer > 0 else 4
        if len(missiles) < missile_limit:
            missiles.append([player_x + player_width // 2 - 5, player_y])

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Level and difficulty scaling
    spawn_timer += 1
    if spawn_timer > FPS * 10:
        level += 1
        spawn_timer = 0

    # Generate resources gradually
    while len(resources) < 5:
        x = random.randint(40, WIDTH - 40)
        y = random.randint(-300, -50)
        rare = random.random() < 0.2
        resources.append([x, y, rare])

    # Generate asteroids gradually
    asteroid_spawn_timer += 1
    spawn_interval = max(30 - level*2, 10)
    if asteroid_spawn_timer > spawn_interval:
        if len(asteroids) < min(3 + level, 12):
            x = random.randint(0, WIDTH - 60)
            speed = random.uniform(1.5 + level*0.3, 3.0 + level*0.4)
            asteroids.append([x, -60, speed])
        asteroid_spawn_timer = 0

    # Generate power-ups gradually
    if random.random() < 0.003:
        x = random.randint(40, WIDTH - 40)
        y = random.randint(-300, -50)
        type_ = random.choice(["shield", "double_score", "rapid_fire"])
        powerups.append([x, y, type_])

    # Move and draw resources
    for resource in resources[:]:
        resource[1] += 2
        img = images["green_resource"] if resource[2] else images["yellow_resource"]
        screen.blit(img, (resource[0]-15, resource[1]-15))
        if player_rect.collidepoint(resource[0], resource[1]):
            points = 150 if resource[2] else 50
            if double_score_timer > 0:
                points *= 2
            score += points
            resources.remove(resource)

    # Move and draw asteroids
    for asteroid in asteroids[:]:
        asteroid[1] += asteroid[2]
        screen.blit(images["asteroid"], (asteroid[0], asteroid[1]))
        asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 60, 60)
        # Collision with player
        if player_rect.colliderect(asteroid_rect) and shield_timer <= 0:
            running = False
        # Collision with missiles
        for missile in missiles[:]:
            missile_rect = pygame.Rect(missile[0], missile[1], 15, 35)
            if asteroid_rect.colliderect(missile_rect):
                if asteroid in asteroids:
                    asteroids.remove(asteroid)
                if missile in missiles:
                    missiles.remove(missile)
                score += 100

    # Move and draw missiles
    for missile in missiles[:]:
        missile[1] -= 8
        screen.blit(images["missile"], (missile[0], missile[1]))
    missiles = [m for m in missiles if m[1] > 0]

    # Move and draw power-ups
    for pu in powerups[:]:
        pu[1] += 2
        img = images[pu[2]]
        screen.blit(img, (pu[0] - img.get_width() // 2, pu[1] - img.get_height() // 2))
        if player_rect.collidepoint(pu[0], pu[1]):
            if pu[2] == "shield":
                shield_timer = FPS * 5
            elif pu[2] == "double_score":
                double_score_timer = FPS * 5
            elif pu[2] == "rapid_fire":
                rapid_fire_timer = FPS * 5
            powerups.remove(pu)

    # Decrease power-up timers
    if shield_timer > 0:
        shield_timer -= 1
    if double_score_timer > 0:
        double_score_timer -= 1
    if rapid_fire_timer > 0:
        rapid_fire_timer -= 1

    # Draw player
    screen.blit(images["spaceship"], (player_x, player_y))

    # Shield glow
    if shield_timer > 0:
        pygame.draw.circle(screen, (0, 255, 255), (player_x + player_width//2, player_y + player_height//2), 50, 3)

    # Display score and level
    score_text = font.render(f"Score: {score}   Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (15, 15))

    pygame.display.flip()
    clock.tick(FPS)

# Game over screen
screen.fill((0, 0, 0))
game_over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(4000)

pygame.quit()
sys.exit()
