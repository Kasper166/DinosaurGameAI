import pygame
import random
import sys

# ── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 300
GROUND_Y      = 250
FPS           = 60

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREY   = (150, 150, 150)
RED    = (200, 50,  50)
GREEN  = (80,  160, 80)

# ── Pixel art dino ────────────────────────────────────────────────────────────
DINO_PIXELS_RUN1 = [
    [0,0,0,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1,0,0,0,0,0],
    [1,1,1,1,1,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0],
]

DINO_PIXELS_RUN2 = [
    [0,0,0,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1,0,0,0,0,0],
    [1,1,1,1,1,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,0,0,0],
    [0,0,1,0,0,1,1,0,0,0,0,0],
    [0,1,1,0,0,0,1,0,0,0,0,0],
]

CACTUS_PIXELS = [
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,1,1,1,1,0,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,1,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [1,1,0,1,1,0,0,0],
    [1,1,1,1,1,0,0,0],
    [1,1,1,1,1,0,0,0],
    [0,0,1,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
]

DINO_PIXELS_DUCK1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,1,0,1,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    
]

DINO_PIXELS_DUCK2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0,0,0],
    [0,1,0,1,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    
]

BIRD_PIXELS_FRAME1 = [
    [0,0,1,1,0,0,0,1,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,1,1,0,0,1,1],
    [0,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0],
]

BIRD_PIXELS_FRAME2 = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0],
]

CACTUS_TALL_PIXELS = [
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,1,1,0],
    [1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,1,1,1,0,0,0,0],
    [0,1,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,1,1,0,0,0,0],
]

CACTUS_DOUBLE_PIXELS = [
    [0,0,1,1,0,0,1,1],
    [0,0,1,1,0,0,1,1],
    [0,1,1,1,0,1,1,1],
    [0,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1],
    [0,0,1,1,1,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,1,1,1,1,0,0],
]

CACTUS_WIDE_PIXELS = [
    [0,0,1,1,0,1,1,0,0,1,1,0],
    [0,0,1,1,0,1,1,0,0,1,1,0],
    [0,1,1,1,0,1,1,0,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,0,1,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
]
PIXEL_SIZE = 4
DINO_W     = 12 * PIXEL_SIZE
DINO_H     = 16 * PIXEL_SIZE
CACTUS_W   = 10  * PIXEL_SIZE
CACTUS_H   = 18 * PIXEL_SIZE
BIRD_W = 12 * PIXEL_SIZE
BIRD_H = 5  * PIXEL_SIZE

def draw_pixel_art(screen, grid, x, y, color):
    for row_i, row in enumerate(grid):
        for col_i, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color,
                    (x + col_i * PIXEL_SIZE,
                     y + row_i * PIXEL_SIZE,
                     PIXEL_SIZE, PIXEL_SIZE))

# ── Dino ──────────────────────────────────────────────────────────────────────
class Dino:
    X = 80

    def __init__(self):
        self.y          = GROUND_Y - DINO_H
        self.vel_y      = 0
        self.is_jumping = False
        self.is_ducking = False
        self.frame      = 0
        self.anim_tick  = 0

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.vel_y      = -18
            self.is_jumping = True

    def duck(self, ducking):
        if not self.is_jumping:
            self.is_ducking = ducking

    def update(self):
        if self.is_jumping:
            self.vel_y += 1
            self.y     += self.vel_y
            if self.y >= GROUND_Y - DINO_H:
                self.y          = GROUND_Y - DINO_H
                self.vel_y      = 0
                self.is_jumping = False

        if not self.is_jumping:
            self.anim_tick += 1
            if self.anim_tick >= 8:
                self.anim_tick = 0
                self.frame     = 1 - self.frame
        
        

    def draw(self, screen):
        if self.is_ducking:
            grid = DINO_PIXELS_DUCK1 if self.frame == 0 else DINO_PIXELS_DUCK2
        else:
            grid = DINO_PIXELS_RUN1 if self.frame == 0 else DINO_PIXELS_RUN2
        draw_pixel_art(screen, grid, self.X, self.y, (83, 83, 83))

    def get_rect(self):
        if self.is_ducking:
            # shorter hitbox when ducking
            return pygame.Rect(self.X + 4, self.y + DINO_H//2, DINO_W - 8, DINO_H//2 - 4)
        return pygame.Rect(self.X + 4, self.y + 4, DINO_W - 8, DINO_H - 8)
# ── Cactus ────────────────────────────────────────────────────────────────────
class Cactus:
    TYPES = [
        (CACTUS_PIXELS,        10,  16),   # original small
        (CACTUS_TALL_PIXELS,   10,  20),   # tall single
        (CACTUS_DOUBLE_PIXELS, 10,  16),   # two cacti close together
        (CACTUS_WIDE_PIXELS,   16, 16),   # three cacti wide
    ]

    def __init__(self, speed):
        grid, cols, rows  = random.choice(self.TYPES)
        self.grid  = grid
        self.w     = cols * PIXEL_SIZE
        self.h     = rows * PIXEL_SIZE
        self.x     = SCREEN_WIDTH + 10
        self.y     = GROUND_Y - self.h
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        draw_pixel_art(screen, self.grid, self.x, self.y, (83, 83, 83))

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.w - 8, self.h - 8)

    def is_off_screen(self):
        return self.x + self.w < 0
class Bird:
    HEIGHTS = [
        GROUND_Y - DINO_H // 2,        # low bird — need to jump over it
        GROUND_Y - DINO_H + 10,    # high bird — need to duck under it
    ]
    def __init__(self, speed):
        self.x         = SCREEN_WIDTH + 10
        self.y         = random.choice(self.HEIGHTS)
        self.speed     = speed + 1
        self.frame     = 0
        self.anim_tick = 0

    def update(self):
        self.x -= self.speed
        self.anim_tick += 1
        if self.anim_tick >= 10:
            self.anim_tick = 0
            self.frame     = 1 - self.frame

    def draw(self, screen):
        grid = BIRD_PIXELS_FRAME1 if self.frame == 0 else BIRD_PIXELS_FRAME2
        draw_pixel_art(screen, grid, self.x, self.y, (83, 83, 83))

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, BIRD_W - 8, BIRD_H - 8)

    def is_off_screen(self):
        return self.x + BIRD_W < 0
# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Game")
    ticker = pygame.time.Clock()
    font   = pygame.font.SysFont(None, 36)

    dino        = Dino()
    obstacles       = []
    score       = 0
    speed       = 7
    spawn_timer = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if not dino.is_jumping:
                        dino.duck(False)

        dino.update()

        # spawning
        spawn_timer += 1
        if spawn_timer >= random.randint(60, 120):
            if score > 300 and random.random() < 0.4:
                obstacles.append(Bird(speed))
            else:
                obstacles.append(Cactus(speed))
            spawn_timer = 0

        # update
        for obs in obstacles:
            obs.update()
        obstacles = [o for o in obstacles if not o.is_off_screen()]

        score += 1
        if score % 500 == 0:
            speed += 1

        for obs in obstacles:
            if dino.get_rect().colliderect(obs.get_rect()):
                running = False

        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        score_text = font.render(f"Score: {score // 10}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH - 160, 20))

        pygame.display.flip()
        ticker.tick(FPS)

    # game over
    screen.fill(WHITE)
    screen.blit(font.render("Game Over!",                   True, BLACK), (SCREEN_WIDTH//2 - 80,  100))
    screen.blit(font.render(f"Final score: {score // 10}", True, GREY),  (SCREEN_WIDTH//2 - 80,  150))
    screen.blit(font.render("R to restart  |  Q to quit",  True, GREY),  (SCREEN_WIDTH//2 - 160, 200))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()