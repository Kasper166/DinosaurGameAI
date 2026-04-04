from turtle import done

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

# ── Pixel art grids ───────────────────────────────────────────────────────────
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
DINO_PIXELS_DUCK1 = [
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
    [0,0,0,0,0,0,0,0,0,0,0,0],
]
DINO_PIXELS_DUCK2 = [
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
    [0,0,0,0,0,0,0,0,0,0,0,0],
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
    [0,0,0,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
    [0,0,0,1,0,0,1,0,0,1,0,0],
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

PIXEL_SIZE = 4
DINO_W     = 12 * PIXEL_SIZE
DINO_H     = 16 * PIXEL_SIZE
CACTUS_H   = 16 * PIXEL_SIZE
BIRD_W     = 12 * PIXEL_SIZE
BIRD_H     =  5 * PIXEL_SIZE

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
        self.y           = GROUND_Y - DINO_H
        self.vel_y       = 0
        self.is_jumping  = False
        self.is_ducking  = False
        self.frame       = 0
        self.anim_tick   = 0
        self.just_landed = False

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.vel_y     = -18
            self.is_jumping = True

    def duck(self, ducking):
        self.is_ducking = ducking

    def update(self):
        self.just_landed = False
        if self.is_jumping:
            self.vel_y += 1
            self.y     += self.vel_y
            if self.y >= GROUND_Y - DINO_H:
                self.y           = GROUND_Y - DINO_H
                self.vel_y       = 0
                self.is_jumping  = False
                self.is_ducking  = False
                self.just_landed = True
        if not self.is_jumping:
            self.anim_tick += 1
            if self.anim_tick >= 4:
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
            return pygame.Rect(self.X + 8, self.y + DINO_H // 2, DINO_W - 16, DINO_H // 2 - 8)
        return pygame.Rect(self.X + 8, self.y + 8, DINO_W - 16, DINO_H - 16)

# ── Cactus ────────────────────────────────────────────────────────────────────
class Cactus:
    TYPES = [
        (CACTUS_PIXELS,        8,  16),
        (CACTUS_TALL_PIXELS,   8,  16),
        (CACTUS_DOUBLE_PIXELS, 8,  16),
        (CACTUS_WIDE_PIXELS,   12, 16),
    ]

    def __init__(self, speed):
        grid, cols, rows = random.choice(self.TYPES)
        self.grid  = grid
        self.w     = cols * PIXEL_SIZE
        self.h     = rows * PIXEL_SIZE
        self.x     = SCREEN_WIDTH + 10
        self.y     = GROUND_Y - self.h
        self.speed = speed
        self.kind  = "cactus"

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        draw_pixel_art(screen, self.grid, self.x, self.y, (83, 83, 83))

    def get_rect(self):
        return pygame.Rect(self.x + 8, self.y + 8, self.w - 16, self.h - 16)

    def is_off_screen(self):
        return self.x + self.w < 0

# ── Bird ──────────────────────────────────────────────────────────────────────
class Bird:
    HEIGHTS = [
        GROUND_Y - DINO_H + 20,    # low bird — must duck
        GROUND_Y - DINO_H - 10,    # low bird — must duck
        GROUND_Y - DINO_H - 100,   # high bird — must jump
    ]

    def __init__(self, speed):
        self.x         = SCREEN_WIDTH + 10
        self.y         = random.choice(self.HEIGHTS)
        self.speed     = speed + 0.5
        self.frame     = 0
        self.anim_tick = 0
        self.kind      = "bird"
        self.passed    = False

    def update(self):
        self.x        -= self.speed
        self.anim_tick += 1
        if self.anim_tick >= 10:
            self.anim_tick = 0
            self.frame     = 1 - self.frame

    def draw(self, screen):
        grid = BIRD_PIXELS_FRAME1 if self.frame == 0 else BIRD_PIXELS_FRAME2
        draw_pixel_art(screen, grid, self.x, self.y, (83, 83, 83))

    def get_rect(self):
        return pygame.Rect(self.x + 8, self.y + 8, BIRD_W - 20, BIRD_H + 2)

    def is_off_screen(self):
        return self.x + BIRD_W < 0

# ── Game environment ──────────────────────────────────────────────────────────
class DinoGame:
    all_time_high = 0

    def __init__(self, render=True):
        self.render_mode = render
        pygame.init()
        if render:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Dino Game")
        else:
            self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont(None, 36)
        self.curriculum_gen = 0
        self.reset()

    def reset(self):
        self.dino        = Dino()
        self.obstacles   = []
        self.score       = 0
        self.speed       = 7
        self.spawn_timer = 0
        self.alive       = True
        return self.get_state()

    def get_state(self):
        ahead = sorted(
            [o for o in self.obstacles if o.x + o.get_rect().width > Dino.X],
            key=lambda o: o.x
        )

        if len(ahead) >= 1:
            n1    = ahead[0]
            dist1 = max(0, n1.x - Dino.X)
            if n1.kind == "bird":
                obs_type1   = 1
                # Normalize bird Y: 0.0 = low (duck), 1.0 = high (jump)
                bird_y_norm1 = (GROUND_Y - n1.y) / SCREEN_HEIGHT
            else:
                obs_type1   = 0
                bird_y_norm1 = 0.0
        else:
            dist1        = SCREEN_WIDTH
            obs_type1   = 0
            bird_y_norm1 = 0.0

        

        frames_away1 = dist1 / self.speed
        if frames_away1 < 20:
            dist_bucket = 0
        elif frames_away1 < 35:
            dist_bucket = 1
        elif frames_away1 < 55:
            dist_bucket = 2
        else:
            dist_bucket = min(3 + int((frames_away1 - 55) // 15), 11)

        is_jumping  = int(self.dino.is_jumping)
        ground_y    = GROUND_Y - DINO_H
        jump_phase  = 0 if not self.dino.is_jumping else min(int((ground_y - self.dino.y) // 20), 3)
        is_ducking  = int(self.dino.is_ducking)

        return (
            dist_bucket,           # 0  how far is obstacle 1
            obs_type1,             # 1  is obstacle 1 a bird?
            bird_y_norm1,          # 2  height of obstacle 1
            is_jumping,            # 3  dino jumping?
            jump_phase,            # 4  how high in the jump
            is_ducking,            # 5  dino ducking?
        )

        
    def step(self, action):
        done   = False
        reward = 1  # per-frame survival reward

        if action == 1:
            self.dino.jump()
        elif action == 2:
            self.dino.duck(True)
        else:
            self.dino.duck(False)

        self.dino.update()
        low_y = max(Bird.HEIGHTS)
        mid_y = Bird.HEIGHTS[1]
        for obs in self.obstacles:
            if obs.kind == "bird":
                                       # bird is close and approaching
                if obs.y == mid_y:               # low or mid bird
                    if self.dino.is_ducking:
                        reward += 10                  # reward every frame it stays ducked
                    else:
                        reward -= 30                   # penalise not ducking
                     
        self.spawn_timer += 1
        
        if self.spawn_timer >= random.randint(40, 60):
            self.spawn_timer = 0

        # ── Curriculum spawn logic ─────────────────────────────────────────
            gen = self.curriculum_gen
            if gen < 40:
                roll = random.random()
                if roll < 0.5:
                    mid_bird = Bird(self.speed)
                    mid_bird.y = Bird.HEIGHTS[1]          # mid height → duck

                    high_bird = Bird(self.speed)
                    high_bird.x = mid_bird.x + 100        # ~180px gap behind the first
                    high_bird.y = Bird.HEIGHTS[2]  
                    self.obstacles.append(mid_bird)
                    self.obstacles.append(high_bird)
                elif roll < 0.8:
                    self.obstacles.append(Bird(self.speed))
                else:
                    self.obstacles.append(Cactus(self.speed))
            elif gen < 80:
                roll = random.random()
                if roll < 0.3:
                    mid_bird = Bird(self.speed)
                    mid_bird.y = Bird.HEIGHTS[1]          # mid height → duck

                    high_bird = Bird(self.speed)
                    high_bird.x = mid_bird.x + 100        # ~180px gap behind the first
                    high_bird.y = Bird.HEIGHTS[2]  
                    self.obstacles.append(mid_bird)
                    self.obstacles.append(high_bird)
                elif roll < 0.5:
                    low_bird = Bird(self.speed)
                    low_bird.y = Bird.HEIGHTS[2]
                    self.obstacles.append(low_bird)
                elif roll < 0.8:
                    self.obstacles.append(Bird(self.speed))
                else:
                    self.obstacles.append(Cactus(self.speed))
            else:   
                roll = random.random()
                if self.score > 100 and roll < 0.6:
                    bird1 = Bird(self.speed)
                    
                    self.obstacles.append(bird1)
                        
                else:
                    self.obstacles.append(Cactus(self.speed))
                
            
            

        
        for obs in self.obstacles:
            obs.update() 

        
 
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
        
        self.score += 1
        if self.score % 500 == 0:
            self.speed += 1
        #print(self.speed)
        for obs in self.obstacles:
            if self.dino.get_rect().colliderect(obs.get_rect()):
                #print("dead")
                done       = True
                reward     = -200
                self.alive = False
                break

        return self.get_state(), reward, done

    def render_frame(self, debug=False):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        self.dino.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score // 10}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 160, 20))

        if debug:
            pygame.draw.rect(self.screen, (255, 0, 0), self.dino.get_rect(), 2)
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, (0, 0, 255), obs.get_rect(), 2)

        if self.render_mode:
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ── Human play mode ───────────────────────────────────────────────────────────
def play():
    game = DinoGame(render=True)
    game.reset()

    while True:
        game.handle_quit()

        action = 0
        keys   = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2

        _, _, done = game.step(action)
        game.render_frame(debug=False) # true voor hitboxes

        if done:
            game.screen.fill(WHITE)
            font = pygame.font.SysFont(None, 36)
            game.screen.blit(font.render("Game Over!", True, BLACK),               (SCREEN_WIDTH//2 - 80,  100))
            game.screen.blit(font.render(f"Score: {game.score // 10}", True, GREY),(SCREEN_WIDTH//2 - 80,  150))
            game.screen.blit(font.render("R to restart  Q to quit", True, GREY),   (SCREEN_WIDTH//2 - 160, 200))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset()
                            waiting = False
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    play()