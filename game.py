import pygame
import random
import sys
import pickle
import json
import os

try:
    import neat
    import numpy as np
    NEAT_AVAILABLE = True
except ImportError:
    NEAT_AVAILABLE = False
    np = None

# ── Constants ────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 300
GROUND_Y      = 250
FPS           = 60

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREY   = (150, 150, 150)
BLUE   = (30,  120, 200)
RED    = (200, 80,  80)
GREEN  = (50,  160, 70)

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

RESTART_PIXELS = [
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,1,0,0,0,0,0,0,1,0,0],
    [0,1,0,0,0,0,0,0,0,0,1,0],
    [1,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,1],
    [0,1,0,0,0,0,0,0,0,0,0,1],
    [0,0,1,0,0,0,0,0,0,0,1,0],
    [0,0,0,1,1,1,1,1,1,1,0,0],
]

PIXEL_SIZE = 4
DINO_W     = 12 * PIXEL_SIZE
DINO_H     = 16 * PIXEL_SIZE
CACTUS_H   = 16 * PIXEL_SIZE
BIRD_W     = 12 * PIXEL_SIZE
BIRD_H     =  5 * PIXEL_SIZE

# ── Difficulty curve (score-based, for human/AI play) ────────────────────────
# display_score = score // 10
BIRD_SCORE_GATE   = 10    # display score before birds appear
SPEED_START       = 6.0
SPEED_MAX         = 18.0
SPEED_INCREMENT   = 1.0    # added every SPEED_STEP display-score points
SPEED_STEP        = 200    # display-score interval between speed bumps
SPAWN_MIN         = 45     # Increased for easier AI learning
SPAWN_MAX_START   = 100    # More spacing


def _spawn_interval_for_speed(speed):
    """Return (min, max) spawn interval given current speed."""
    t = (speed - SPEED_START) / (SPEED_MAX - SPEED_START)
    t = max(0.0, min(1.0, t))
    hi = int(SPAWN_MAX_START - t * (SPAWN_MAX_START - SPAWN_MIN))
    lo = max(SPAWN_MIN, hi - 20)
    return lo, hi


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
            self.vel_y      = -18
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

    def draw(self, screen, color=(83, 83, 83)):
        if self.is_ducking:
            grid = DINO_PIXELS_DUCK1 if self.frame == 0 else DINO_PIXELS_DUCK2
        else:
            grid = DINO_PIXELS_RUN1 if self.frame == 0 else DINO_PIXELS_RUN2
        draw_pixel_art(screen, grid, self.X, self.y, color)

    def get_rect(self):
        if self.is_ducking:
            # Use a hitbox that matches the ducking sprite's visual dimensions.
            return pygame.Rect(self.X, self.y + DINO_H // 2, DINO_W, DINO_H // 2)
        return pygame.Rect(self.X, self.y, DINO_W, DINO_H)


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
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_off_screen(self):
        return self.x + self.w < 0


# ── Bird ──────────────────────────────────────────────────────────────────────
class Bird:
    # Ground-level (must duck), mid (must duck), high (run under freely)
    HEIGHTS = [
        GROUND_Y - DINO_H + 20,          # low  – must jump
        GROUND_Y - DINO_H - 10,          # mid  – must duck
        GROUND_Y - DINO_H - 100,         # high – run under
    ]

    def __init__(self, speed):
        self.x         = SCREEN_WIDTH + 10
        self.y         = random.choice(self.HEIGHTS)
        self.speed     = speed + 0.5
        self.frame     = 0
        self.anim_tick = 0
        self.kind      = "bird"
        self.passed    = False
        self.w         = BIRD_W
        self.h         = BIRD_H

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
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_off_screen(self):
        return self.x + BIRD_W < 0


# ── Game environment ──────────────────────────────────────────────────────────
class DinoGame:
    all_time_high = 0

    def __init__(self, render=True):
        self.render_mode    = render
        self.use_score_curve = True   # False → curriculum_gen for NEAT training
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
        self.dino           = Dino()
        self.obstacles      = []
        self.score          = 0
        self.alive          = True
        self.spawn_timer    = 0
        self._next_spawn    = random.randint(30, 50)
        self._last_speed_milestone = 0
        if self.use_score_curve:
            self.speed = SPEED_START
        else:
            self.speed = 7
        self._last_dino_y = self.dino.y
        return self.get_state()

    # ── Spawn logic ───────────────────────────────────────────────────────────
    def _spawn_obstacle(self):
        display_score = self.score // 10
        bird_ok = display_score >= BIRD_SCORE_GATE

        # The logic for spawning obstacles based on whether it's for human play or AI training.
        if self.use_score_curve:
            roll = random.random()
            # Clusters can now spawn from the beginning.
            
            # Birds only appear after a certain score.
            if bird_ok and roll < 0.40: # 25% chance for a bird (0.40 - 0.15)
                self.obstacles.append(Bird(self.speed))
            # Default to a single cactus.
            else: # 60% chance for a cactus
                self.obstacles.append(Cactus(self.speed))
        else:
            # Progressive curriculum for NEAT training
            gen = self.curriculum_gen
            roll = random.random()
            
            if gen < 10:
                
                if roll < 0.5:
                    # Phase 0: PURE DUCKING (100% Birds)
                    bird = Bird(self.speed)
                    bird.y = Bird.HEIGHTS[2] # Forced Mid-Height
                    self.obstacles.append(bird)
                elif roll < 0.8: 
                    bird = Bird(self.speed)
                    bird.y = Bird.HEIGHTS[0] # Forced Mid-Height
                    self.obstacles.append(bird)
                else:
                    bird = Bird(self.speed)
                    bird.y = Bird.HEIGHTS[1] # Forced Mid-Height
                    self.obstacles.append(bird)
            elif gen < 26:
                # Phase 1: Mostly Birds + Some Cacti
                if roll < 0.7:
                    bird = Bird(self.speed)
                    self.obstacles.append(bird)
                else:
                    self.obstacles.append(Cactus(self.speed))

            else:
                # Phase 2: Simple mix with clusters
                if roll < 0.3:
                    self.obstacles.append(Bird(self.speed))
                
                else:
                    self.obstacles.append(Cactus(self.speed))

    def get_state(self, dino=None):
        if dino is None: dino = self.dino
            
        ahead = sorted([o for o in self.obstacles if o.x + o.w > Dino.X], key=lambda o: o.x)
        sensors = [0.0] * 5
        
        # 0: DIST 1 (0.0 to 1.0)
        if len(ahead) > 0:
            o = ahead[0]
            sensors[0] = (o.x - Dino.X) / SCREEN_WIDTH
            # 1: TYPE 1 (Cactus=0.5, Bird=1.0)
            sensors[1] = 0.5 if o.kind == "cactus" else 1.0
        # 2: SIZE 1 (More spread for birds: 0.2, 0.5, 0.8)
        if len(ahead) > 0:
            o = ahead[0]
            if o.kind == "cactus":
                sensors[2] = o.w / 100.0
            else:
                h = GROUND_Y - o.y
                if h < 55: sensors[2] = 0.2     # Low Bird (h=44)
                elif h < 110: sensors[2] = 0.5   # Mid Bird (h=74)
                else: sensors[2] = 0.8          # High Bird (h=164)
        else:
            sensors[2] = 0.0
            
        # 3: DINO Y
        sensors[3] = (GROUND_Y - dino.y) / 150.0
        
        # 4: SPEED
        sensors[4] = (self.speed - SPEED_START) / (SPEED_MAX - SPEED_START)
        
        return tuple(sensors)

    def step(self, action):
        done   = False
        reward = 1

        if action == 1:
            self.dino.jump()
        elif action == 2:
            self.dino.duck(True)
        else:
            self.dino.duck(False)

        self.dino.update()

        # Ducking Reward Shaping (Crucial for learning Mid-Birds)
        mid_y = Bird.HEIGHTS[1]
        for obs in self.obstacles:
            if obs.kind == "bird" and abs(obs.x - self.dino.X) < 100:
                if obs.y == mid_y:
                    if self.dino.is_ducking:
                        reward += 0.5   # Small continuous bonus for doing it right
                    elif not self.dino.is_jumping:
                        reward -= 1.0   # Penalty for standing still under a mid-bird
        # Speed ramp (score-based curve)
        self.score += 1
        if self.use_score_curve:
            display_score = self.score // 10
            milestone = (display_score // SPEED_STEP) * SPEED_STEP
            if milestone > self._last_speed_milestone and display_score > 0:
                self._last_speed_milestone = milestone
                self.speed = min(SPEED_MAX, self.speed + SPEED_INCREMENT)
        else:
            if self.score % 500 == 0:
                self.speed = min(18, self.speed + 1)

        # Spawn
        self.spawn_timer += 1
        if self.spawn_timer >= self._next_spawn:
            self.spawn_timer = 0
            lo, hi = _spawn_interval_for_speed(self.speed) if self.use_score_curve else (40, 60)
            self._next_spawn = random.randint(lo, hi)
            self._spawn_obstacle()

        # Update & prune
        for obs in self.obstacles:
            obs.update()
            if not getattr(obs, 'passed', False) and obs.x < self.dino.X:
                obs.passed = True
                reward += 50.0  # Big bonus for successfully clearing an obstacle

        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # Collision — tight inner loop
        dino_rect = self.dino.get_rect()
        for obs in self.obstacles:
            if dino_rect.colliderect(obs.get_rect()):
                done       = True
                reward     = -200
                self.alive = False
                break

        return self.get_state(), reward, done

    def render_frame(self, extra_draw=None, debug=False):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        self.dino.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score // 10:05d}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 175, 20))

        if extra_draw:
            extra_draw(self.screen)

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


# ── AI Loader ─────────────────────────────────────────────────────────────────
def load_ai():
    """Load best genome. Returns (net, generation, fitness). Returns (None,0,0) on failure."""
    if not NEAT_AVAILABLE:
        return None, 0, 0
    if not os.path.exists("best_genome.pkl") or not os.path.exists("neat_config.txt"):
        return None, 0, 0
    try:
        config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            "neat_config.txt"
        )
        with open("best_genome.pkl", "rb") as f:
            genome = pickle.load(f)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        gen, fit = 0, 0
        if os.path.exists("best_genome_meta.json"):
            with open("best_genome_meta.json") as f:
                meta = json.load(f)
            gen = meta.get("generation", 0)
            fit = meta.get("fitness", 0)
        return net, gen, fit
    except Exception:
        return None, 0, 0


def get_ai_action(net, game, dino):
    """Compute AI action for a specific dino using current game state."""
    inputs = game.get_state(dino)
    output = net.activate(inputs)
    return int(np.argmax(output))

# ── Visual Analytics ──────────────────────────────────────────────────────────
def draw_network(screen, net, pos=(650, 16), size=(230, 140)):
    """Render the neural network with a professional blue color palette."""
    if not net: return
    x, y = pos
    w, h = size
    
    # Simple transluscent backdrop
    surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 255, 255, 180), (0, 0, w, h), border_radius=10)
    pygame.draw.rect(surface, (200, 200, 200, 255), (0, 0, w, h), 1, border_radius=10)
    screen.blit(surface, (x, y))
    
    # Node mapping
    node_positions = {}
    input_ids = sorted([i for i in net.input_nodes])
    output_ids = sorted([o for o in net.output_nodes])
    
    # Position sensors (left)
    for i, nid in enumerate(input_ids):
        node_positions[nid] = (x + 20, y + 20 + i * (h - 40) / max(1, len(input_ids) - 1))
    
    # Position actions (right)
    for i, nid in enumerate(output_ids):
        node_positions[nid] = (x + w - 20, y + 28 + i * (h - 56) / max(1, len(output_ids) - 1))
        
    # Draw connections
    for node_id, _, _, _, _, links in net.node_evals:
        if node_id not in node_positions:
            node_positions[node_id] = (x + w/2, y + h/2 + (node_id * 12 % (h-40)))
            
        target_pos = node_positions[node_id]
        for input_id, weight in links:
            if input_id in node_positions:
                start_pos = node_positions[input_id]
                # Professional blue tones: light for positive, dark for negative
                color = (100, 180, 255) if weight > 0 else (40, 80, 160)
                thickness = int(max(1, min(5, abs(weight) * 2)))
                pygame.draw.line(screen, color, start_pos, target_pos, thickness)

    SENSOR_LABELS = { 
        -1: "DIST1", -2: "TYPE1", -3: "SIZE1", -4: "DINO_Y", -5: "SPEED"
    }
    ACTION_LABELS = { 0: "RUN", 1: "JUMP", 2: "DUCK" }
    
    # Draw nodes
    font = pygame.font.SysFont(None, 18)
    for nid, pos in node_positions.items():
        pygame.draw.circle(screen, (30, 120, 255), (int(pos[0]), int(pos[1])), 6)
        pygame.draw.circle(screen, (0, 0, 0), (int(pos[0]), int(pos[1])), 6, 1)
        
        # Node Labels
        lbl_text = ""
        if nid in SENSOR_LABELS:
            lbl_text = SENSOR_LABELS[nid]
            screen.blit(font.render(lbl_text, True, (80, 80, 80)), (pos[0] - 35, pos[1] - 5))
        elif nid in ACTION_LABELS:
            lbl_text = ACTION_LABELS[nid]
            screen.blit(font.render(lbl_text, True, (80, 80, 80)), (pos[0] + 12, pos[1] - 5))

    # General Labels
    title_font = pygame.font.SysFont(None, 14, bold=True)
    screen.blit(title_font.render("SENSORS", True, (150, 150, 150)), (x + 10, y + 5))
    screen.blit(title_font.render("ACTIONS", True, (150, 150, 150)), (x + w - 60, y + 5))


def step_extra_dino(dino, action, obstacles):
    """Apply action + update for a dino not owned by DinoGame. Returns True if dead."""
    if action == 1:
        dino.jump()
    elif action == 2:
        dino.duck(True)
    else:
        dino.duck(False)
    dino.update()
    dino_rect = dino.get_rect()
    for obs in obstacles:
        if dino_rect.colliderect(obs.get_rect()):
            return True
    return False


# ── Training history loader ───────────────────────────────────────────────────
def load_training_history():
    """Return list of generation dicts from training_history.json, or []."""
    if not os.path.exists("training_history.json"):
        return []
    try:
        with open("training_history.json") as f:
            return json.load(f)
    except Exception:
        return []


# ── Inline Pygame bar chart ───────────────────────────────────────────────────
def _draw_bar_chart(surf, x, y, w, h, history, player_score):
    """Draw a compact fitness-vs-generation bar chart onto surf."""
    if not history:
        return

    font_tiny = pygame.font.SysFont(None, 20)
    bests = [rec["best"] for rec in history]
    avgs  = [rec["avg"]  for rec in history]
    peak  = max(bests) if bests else 1

    bg = pygame.Surface((w, h), pygame.SRCALPHA)
    bg.fill((245, 245, 245, 220))
    surf.blit(bg, (x, y))
    pygame.draw.rect(surf, (180, 180, 180), (x, y, w, h), 1)

    # Axes
    axis_x = x + 40
    axis_y = y + h - 30
    chart_w = w - 50
    chart_h = h - 40

    pygame.draw.line(surf, BLACK, (axis_x, y + 10), (axis_x, axis_y), 1)
    pygame.draw.line(surf, BLACK, (axis_x, axis_y), (axis_x + chart_w, axis_y), 1)

    n = len(history)
    bar_w = max(2, chart_w // n - 1)

    for i, rec in enumerate(history):
        bx = axis_x + int(i * chart_w / n)
        # Best bar (blue)
        bh = int(rec["best"] / peak * chart_h)
        pygame.draw.rect(surf, (30, 120, 200),
                         (bx, axis_y - bh, bar_w, bh))
        # Avg bar (grey overlay)
        ah = int(rec["avg"] / peak * chart_h)
        pygame.draw.rect(surf, (160, 160, 160),
                         (bx, axis_y - ah, max(1, bar_w - 1), ah))

    # Player score line
    if player_score is not None and peak > 0:
        player_frames = player_score  # score in raw frames
        py = axis_y - int(player_frames / peak * chart_h)
        py = max(y + 10, min(axis_y, py))
        pygame.draw.line(surf, RED, (axis_x, py), (axis_x + chart_w, py), 2)
        lbl = font_tiny.render(f"You: {player_score // 10}", True, RED)
        surf.blit(lbl, (axis_x + chart_w - lbl.get_width() - 2, py - 14))

    # Labels
    peak_lbl = font_tiny.render(f"{int(peak)}", True, GREY)
    surf.blit(peak_lbl, (x + 2, y + 10))
    x_lbl = font_tiny.render(f"Gen 1", True, GREY)
    surf.blit(x_lbl, (axis_x, axis_y + 4))
    xn_lbl = font_tiny.render(f"Gen {n}", True, GREY)
    surf.blit(xn_lbl, (axis_x + chart_w - xn_lbl.get_width(), axis_y + 4))


# ── Post-Game Analytics Screen ────────────────────────────────────────────────
def show_analytics_screen(screen, clock, player_score, ai_score, ai_gen, ai_fit):
    """
    Full-window post-game analytics. player_score / ai_score are raw frame counts.
    Returns 'restart' or 'menu'.
    """
    history      = load_training_history()
    font_big     = pygame.font.SysFont(None, 56)
    font_med     = pygame.font.SysFont(None, 34)
    font_sm      = pygame.font.SysFont(None, 26)

    display_ps   = player_score // 10
    display_ai   = (ai_score // 10) if ai_score is not None else None

    # Find first gen that beat the player's score
    first_beat_gen = None
    if history:
        for rec in history:
            if rec.get("best", 0) >= player_score:
                first_beat_gen = rec["gen"]
                break

    avg_fit  = int(sum(r["avg"]  for r in history) / len(history)) if history else 0
    peak_fit = int(max(r["best"] for r in history))                 if history else 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return "menu"

        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        # Title
        go = font_big.render("GAME  OVER", True, BLACK)
        screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, 12))

        # Restart icon
        icon_x = SCREEN_WIDTH // 2 - len(RESTART_PIXELS[0]) * PIXEL_SIZE // 2
        draw_pixel_art(screen, RESTART_PIXELS, icon_x, 68, BLACK)

        # Score row
        y = 108
        ps_surf = font_med.render(f"Your score: {display_ps:,}", True, BLACK)
        screen.blit(ps_surf, (SCREEN_WIDTH // 2 - ps_surf.get_width() // 2, y))

        if display_ai is not None:
            gen_str = f"Gen {ai_gen}" if ai_gen else "AI"
            if display_ai > display_ps:
                msg   = f"{gen_str} beat you  ({display_ai:,})"
                col   = RED
            elif display_ai < display_ps:
                msg   = f"You beat the AI!  ({gen_str} scored {display_ai:,})"
                col   = GREEN
            else:
                msg   = f"Tie with {gen_str}!  Both: {display_ps:,}"
                col   = BLUE
            ai_surf = font_sm.render(msg, True, col)
            screen.blit(ai_surf, (SCREEN_WIDTH // 2 - ai_surf.get_width() // 2, y + 30))

        # Analytics strip
        if history:
            _draw_bar_chart(screen, 20, 148, 540, 88, history, player_score)

            # Stat cards on right
            cx = 580
            cards = [
                ("Peak AI",      f"{peak_fit // 10:,}",  BLUE),
                ("Avg AI",       f"{avg_fit  // 10:,}",  GREY),
                ("Generations",  f"{len(history)}",      BLACK),
            ]
            if first_beat_gen is not None:
                cards.append(("AI beat you at",  f"Gen {first_beat_gen}", RED))

            for ci, (label, val, col) in enumerate(cards):
                cy = 150 + ci * 46
                pygame.draw.rect(screen, (240, 244, 250), (cx, cy, 300, 38), border_radius=6)
                pygame.draw.rect(screen, (200, 210, 230), (cx, cy, 300, 38), 1, border_radius=6)
                lbl_s = font_sm.render(label, True, GREY)
                val_s = font_med.render(val,   True, col)
                screen.blit(lbl_s, (cx + 10,  cy + 4))
                screen.blit(val_s, (cx + 300 - val_s.get_width() - 10, cy + 6))
        else:
            note = font_sm.render("Train the AI first to see analytics  (neat_train.py)", True, GREY)
            screen.blit(note, (SCREEN_WIDTH // 2 - note.get_width() // 2, 170))

        hint = font_sm.render("[R] Restart     [ESC] Menu", True, GREY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, GROUND_Y + 8))

        pygame.display.flip()
        clock.tick(FPS)


# ── Human play ────────────────────────────────────────────────────────────────
def play(show_ai=False):
    """Human play mode. AI runs silently; [T] toggles its visibility."""
    net, ai_gen, ai_fit = load_ai()
    game = DinoGame(render=True)
    game.use_score_curve = True
    game.reset()

    ai_dino      = Dino() if net else None
    ai_alive     = net is not None
    ai_score     = None
    show_ai_dino = show_ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and net:
                    show_ai_dino = not show_ai_dino
                if event.key == pygame.K_ESCAPE:
                    return

        keys   = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2

        _, _, done = game.step(action)
        state      = game.get_state()

        if ai_alive and net:
            ai_action = get_ai_action(net, game, ai_dino)
            dead      = step_extra_dino(ai_dino, ai_action, game.obstacles)
            if dead:
                ai_alive = False
                ai_score = game.score

        def extra(surf):
            if show_ai_dino and net:
                col = BLUE if ai_alive else (180, 180, 220)
                ai_dino.draw(surf, col)
                draw_network(surf, net)
            hint_font = pygame.font.SysFont(None, 22)
            hint_col  = (30, 130, 200) if show_ai_dino else GREY
            label     = "T: hide AI" if show_ai_dino else "T: show AI"
            surf.blit(hint_font.render(label, True, hint_col), (10, 16))

        game.render_frame(extra_draw=extra)

        if done:
            final_ai = ai_score if not ai_alive else game.score
            if not net:
                final_ai = None
            result = show_analytics_screen(
                game.screen, game.clock,
                game.score, final_ai, ai_gen, ai_fit
            )
            if result == "restart":
                game.reset()
                if net:
                    ai_dino  = Dino()
                    ai_alive = True
                    ai_score = None
            else:
                return


# ── Play vs AI ────────────────────────────────────────────────────────────────
def play_vs_ai():
    """Human and AI run side by side. AI always visible."""
    net, ai_gen, ai_fit = load_ai()
    if not net:
        play(show_ai=False)
        return

    game = DinoGame(render=True)
    game.use_score_curve = True
    game.reset()

    ai_dino  = Dino()
    ai_alive = True
    ai_score = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys   = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2

        _, _, done = game.step(action)
        state      = game.get_state()

        if ai_alive:
            ai_action = get_ai_action(net, game, ai_dino)
            dead      = step_extra_dino(ai_dino, ai_action, game.obstacles)
            if dead:
                ai_alive = False
                ai_score = game.score

        def extra(surf):
            col = BLUE if ai_alive else (180, 180, 220)
            ai_dino.draw(surf, col)
            draw_network(surf, net)
            font_sm = pygame.font.SysFont(None, 22)
            gen_str = f"Gen {ai_gen}" if ai_gen else "AI"
            surf.blit(font_sm.render(f"■ {gen_str}", True, BLUE),        (10, 16))
            surf.blit(font_sm.render("■ You",        True, (83, 83, 83)), (10, 34))

        game.render_frame(extra_draw=extra)

        if done:
            final_ai = game.score if ai_alive else ai_score
            result = show_analytics_screen(
                game.screen, game.clock,
                game.score, final_ai, ai_gen, ai_fit
            )
            if result == "restart":
                game.reset()
                ai_dino  = Dino()
                ai_alive = True
                ai_score = None
            else:
                return


# ── Watch Best Genome ─────────────────────────────────────────────────────────
def play_best_genome():
    """Watch the best trained genome play autonomously."""
    net, ai_gen, ai_fit = load_ai()
    if not net:
        return

    game = DinoGame(render=True)
    game.use_score_curve = True
    game.reset()
    fast_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_f:
                    fast_mode = not fast_mode

        action = get_ai_action(net, game, game.dino)
        _, _, done = game.step(action)

        def extra(surf):
            draw_network(surf, net)
            font_sm = pygame.font.SysFont(None, 22)
            gen_str = f"Gen {ai_gen}" if ai_gen else "AI"
            fit_str = f"Fitness: {ai_fit // 10:,}" if ai_fit else ""
            surf.blit(font_sm.render(f"Watching: {gen_str}  {fit_str}", True, BLUE), (10, 16))
            mode_col = (200, 100, 30) if fast_mode else GREY
            surf.blit(font_sm.render("F: fast ON" if fast_mode else "F: fast mode", True, mode_col), (10, 34))
            surf.blit(font_sm.render("ESC: menu", True, GREY), (10, 52))

        if fast_mode:
            # Minimal draw in fast mode
            game.screen.fill(WHITE)
            pygame.draw.line(game.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
            game.dino.draw(game.screen, BLUE)
            for obs in game.obstacles:
                obs.draw(game.screen)
            score_text = game.font.render(f"Score: {game.score // 10:05d}", True, BLACK)
            game.screen.blit(score_text, (SCREEN_WIDTH - 175, 20))
            extra(game.screen)
            pygame.display.flip()
            game.clock.tick(0)
        else:
            game.render_frame(extra_draw=extra)

        if done:
            result = show_analytics_screen(
                game.screen, game.clock,
                game.score, game.score, ai_gen, ai_fit
            )
            if result == "restart":
                game.reset()
            else:
                return


# ── Generation Demo (Spectator) ───────────────────────────────────────────────
def demo_generation():
    """Watch the entire last training generation play side by side."""
    if not NEAT_AVAILABLE:
        return
    if not os.path.exists("last_generation.pkl") or not os.path.exists("neat_config.txt"):
        return

    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        "neat_config.txt"
    )
    with open("last_generation.pkl", "rb") as f:
        genomes = pickle.load(f)

    COLOR_ALIVE = (83,  83, 83)
    COLOR_BEST  = (30, 120, 200)
    COLOR_LAST  = (200, 80,  80)

    best_genome_id = max(genomes, key=lambda x: x[1].fitness or 0)[0]
    nets = [(neat.nn.FeedForwardNetwork.create(g, config), g, gid) for gid, g in genomes]
    n    = len(nets)

    master = DinoGame(render=True)
    master.use_score_curve = True
    master.reset()

    dinos     = [Dino() for _ in range(n)]
    alive     = [True] * n
    clock     = pygame.time.Clock()
    font_sm   = pygame.font.SysFont(None, 24)
    font_med  = pygame.font.SysFont(None, 36)
    fast_mode = False

    best_dino_index = next(
        (i for i, (_, _, gid) in enumerate(nets) if gid == best_genome_id), 0
    )

    while any(alive):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fast_mode = not fast_mode
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return

        master_state = master.get_state()

        for i, (net, genome, gid) in enumerate(nets):
            if not alive[i]:
                continue
            dino = dinos[i]
            action = get_ai_action(net, master, dino)
            if step_extra_dino(dino, action, master.obstacles):
                alive[i] = False

        master.step(0)

        best_alive_index   = None
        best_alive_fitness = -1
        for i, (_, genome, _) in enumerate(nets):
            if alive[i]:
                fit = genome.fitness or 0
                if fit > best_alive_fitness:
                    best_alive_fitness = fit
                    best_alive_index   = i
        alive_count = sum(alive)

        master.screen.fill(WHITE)
        pygame.draw.line(master.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        for obs in master.obstacles:
            obs.draw(master.screen)
        
        # Draw network for the best current survivor
        if best_alive_index is not None:
            draw_network(master.screen, nets[best_alive_index][0])

        for i, dino in enumerate(dinos):
            if not alive[i]:
                continue
            _, genome, gid = nets[i]
            if alive_count == 1:
                color = COLOR_LAST
            elif gid == best_genome_id and alive[best_dino_index]:
                color = COLOR_BEST
            elif i == best_alive_index and not alive[best_dino_index]:
                color = COLOR_BEST
            else:
                color = COLOR_ALIVE
            dino.draw(master.screen, color)

        master.screen.blit(font_med.render(f"Score: {master.score // 10:05d}", True, BLACK), (SCREEN_WIDTH - 175, 16))
        master.screen.blit(font_sm.render(f"Alive: {alive_count} / {n}",    True, GREY),  (SCREEN_WIDTH - 175, 52))
        master.screen.blit(font_sm.render(f"Speed: {master.speed:.1f}",      True, GREY),  (SCREEN_WIDTH - 175, 72))
        master.screen.blit(font_sm.render(
            "F: fast ON" if fast_mode else "F: fast mode",
            True, (200, 100, 30) if fast_mode else GREY), (10, 16))
        master.screen.blit(font_sm.render("ESC: menu", True, GREY), (10, 36))

        bar_w = 180
        bar_x, bar_y = SCREEN_WIDTH - 175, 96
        pygame.draw.rect(master.screen, (220, 220, 220), (bar_x, bar_y, bar_w, 8), border_radius=4)
        fill = int(bar_w * alive_count / n) if n > 0 else 0
        if fill > 0:
            pygame.draw.rect(master.screen, (83, 150, 83), (bar_x, bar_y, fill, 8), border_radius=4)

        pygame.draw.rect(master.screen, COLOR_BEST, (10, 58, 10, 10))
        master.screen.blit(font_sm.render("Best genome", True, GREY), (24, 56))
        pygame.draw.rect(master.screen, COLOR_LAST, (10, 74, 10, 10))
        master.screen.blit(font_sm.render("Last alive",  True, GREY), (24, 72))

        pygame.display.flip()
        clock.tick(0 if fast_mode else FPS)


# ── Main Menu ─────────────────────────────────────────────────────────────────
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dinosaur AI")
    clock  = pygame.time.Clock()

    font_title = pygame.font.SysFont(None, 52)
    font_sub   = pygame.font.SysFont(None, 30)
    font_sm    = pygame.font.SysFont(None, 24)

    has_ai   = os.path.exists("best_genome.pkl") and NEAT_AVAILABLE
    has_demo = os.path.exists("last_generation.pkl") and NEAT_AVAILABLE

    _, ai_gen, ai_fit = load_ai() if has_ai else (None, 0, 0)

    anim_tick  = 0
    dino_frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play(show_ai=False)
                elif event.key == pygame.K_a and has_ai:
                    play_vs_ai()
                elif event.key == pygame.K_w and has_ai:
                    play_best_genome()
                elif event.key == pygame.K_d and has_demo:
                    demo_generation()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        anim_tick += 1
        if anim_tick >= 8:
            anim_tick  = 0
            dino_frame = 1 - dino_frame

        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        grid = DINO_PIXELS_RUN1 if dino_frame == 0 else DINO_PIXELS_RUN2
        draw_pixel_art(screen, grid, 80, GROUND_Y - DINO_H, (83, 83, 83))

        title = font_title.render("DINOSAUR   AI", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        sub = font_sub.render("NEAT-powered evolution", True, GREY)
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 84))

        gen_info = f"  (Gen {ai_gen})" if ai_gen else ""
        fit_info = f"  fitness {ai_fit // 10:,}" if ai_fit else ""
        opts = [
            ("[SPACE]  Play",                       True,     BLACK,                  145),
            ("[A]      Play vs AI" + gen_info,       has_ai,   BLUE  if has_ai else GREY, 178),
            ("[W]      Watch AI" + fit_info,         has_ai,   (0,140,80) if has_ai else GREY, 211),
            ("[D]      Spectator — full generation", has_demo, (130,60,180) if has_demo else GREY, 244),
        ]
        for label, enabled, color, y in opts:
            surf = font_sub.render(label, True, color if enabled else GREY)
            screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))

        if not has_ai:
            note = font_sm.render("(No best_genome.pkl — run neat_train.py first)", True, (200, 120, 50))
            screen.blit(note, (SCREEN_WIDTH // 2 - note.get_width() // 2, GROUND_Y + 8))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()