import neat
import pickle
import numpy as np
import pygame
from game import (DinoGame, Dino, GROUND_Y, DINO_H, SCREEN_WIDTH, SCREEN_HEIGHT,
                  WHITE, BLACK, GREY, FPS, PIXEL_SIZE,
                  DINO_PIXELS_RUN1, DINO_PIXELS_RUN2, DINO_PIXELS_DUCK1, DINO_PIXELS_DUCK2,
                  draw_pixel_art, BIRD_W)

COLOR_ALIVE = (83,  83,  83)
COLOR_BEST  = (30,  120, 200)
COLOR_LAST  = (200, 80,  80)

def replay():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    with open("last_generation.pkl", "rb") as f:
        genomes = pickle.load(f)

    best_genome_id = max(genomes, key=lambda x: x[1].fitness or 0)[0]
    nets = [(neat.nn.FeedForwardNetwork.create(g, config), g, gid) for gid, g in genomes]
    n    = len(nets)

    master = DinoGame(render=True)
    master.reset()

    dinos      = [Dino() for _ in range(n)]
    alive      = [True] * n
    clock      = pygame.time.Clock()
    font_sm    = pygame.font.SysFont(None, 24)
    font_med   = pygame.font.SysFont(None, 36)
    font_mono  = pygame.font.SysFont("Courier New", 18)
    fast_mode  = False
    debug_mode = False

    while any(alive):

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fast_mode = not fast_mode
                if event.key == pygame.K_d:
                    debug_mode = not debug_mode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        master_state = master.get_state()

        # ── Nearest obstacle info for debug ───────────────────────────────────
        ahead = sorted(
            [o for o in master.obstacles if o.x + o.get_rect().width > Dino.X],
            key=lambda o: o.x
        )
        nearest = ahead[0] if ahead else None
        if nearest:
            if nearest.kind == "bird":
                height_label = "HIGH" if nearest.y < GROUND_Y - DINO_H - 20 else "LOW/MID"
                obs_desc = f"BIRD {height_label}  y={nearest.y}  dist={int(nearest.x - Dino.X)}"
            else:
                obs_desc = f"CACTUS  dist={int(nearest.x - Dino.X)}"
        else:
            obs_desc = "none"

        # ── Find best original genome index ───────────────────────────────────
        best_dino_index = next(
            (i for i, (_, _, gid) in enumerate(nets) if gid == best_genome_id), 0
        )

        # ── Step each dino ────────────────────────────────────────────────────
        for i, (net, genome, gid) in enumerate(nets):
            if not alive[i]:
                continue

            dino       = dinos[i]
            
            inputs = master.get_state(dino)

            output = net.activate(inputs)
            action = int(np.argmax(output))

            if action == 1:
                dino.jump()
            elif action == 2:
                dino.duck(True)
            else:
                dino.duck(False)

            dino.update()

            for obs in master.obstacles:
                if dino.get_rect().colliderect(obs.get_rect()):
                    alive[i] = False
                    break

        master.step(0)

        # ── Find best still-alive dino ────────────────────────────────────────
        best_alive_index    = None
        best_alive_fitness  = -1
        for i, (_, genome, gid) in enumerate(nets):
            if alive[i]:
                fit = genome.fitness or 0
                if fit > best_alive_fitness:
                    best_alive_fitness = fit
                    best_alive_index   = i

        alive_count = sum(alive)

        # ── Draw ──────────────────────────────────────────────────────────────
        master.screen.fill(WHITE)
        pygame.draw.line(master.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        for obs in master.obstacles:
            obs.draw(master.screen)

        # draw dinos (only once, with correct color)
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
            grid = (DINO_PIXELS_DUCK1 if dino.frame == 0 else DINO_PIXELS_DUCK2) if dino.is_ducking \
                   else (DINO_PIXELS_RUN1 if dino.frame == 0 else DINO_PIXELS_RUN2)
            draw_pixel_art(master.screen, grid, dino.X, dino.y, color)

        # ── HUD ───────────────────────────────────────────────────────────────
        master.screen.blit(font_med.render(f"Score: {master.score // 10}", True, BLACK), (SCREEN_WIDTH - 170, 16))
        master.screen.blit(font_sm.render(f"Alive: {alive_count} / {n}",  True, GREY),  (SCREEN_WIDTH - 170, 52))
        master.screen.blit(font_sm.render(f"Speed: {master.speed}",        True, GREY),  (SCREEN_WIDTH - 170, 76))
        master.screen.blit(font_sm.render("F: fast ON" if fast_mode else "F: fast",
                           True, (200, 100, 30) if fast_mode else GREY), (10, 16))
        master.screen.blit(font_sm.render("D: debug ON" if debug_mode else "D: debug",
                           True, (30, 150, 80) if debug_mode else GREY), (10, 40))

        bar_w = 180
        bar_x, bar_y = SCREEN_WIDTH - 170, 104
        pygame.draw.rect(master.screen, (220, 220, 220), (bar_x, bar_y, bar_w, 8), border_radius=4)
        fill = int(bar_w * alive_count / n)
        if fill > 0:
            pygame.draw.rect(master.screen, (83, 150, 83), (bar_x, bar_y, fill, 8), border_radius=4)

        pygame.draw.rect(master.screen, COLOR_BEST, (10, 66, 10, 10))
        master.screen.blit(font_sm.render("Best genome", True, GREY), (24, 64))
        pygame.draw.rect(master.screen, COLOR_LAST, (10, 84, 10, 10))
        master.screen.blit(font_sm.render("Last alive",  True, GREY), (24, 82))

        # ── Debug overlay ──────────────────────────────────────────────────────
        if debug_mode and best_alive_index is not None:
            best_dino  = dinos[best_alive_index]
            ground_y   = GROUND_Y - DINO_H
            jump_phase = 0 if not best_dino.is_jumping else min(int((ground_y - best_dino.y) // 20), 3)
            
            inputs = master.get_state(best_dino)
            output     = nets[best_alive_index][0].activate(inputs)
            action     = int(np.argmax(output))
            action_lbl = ["RUN", "JUMP", "DUCK"][action]

            _, watched_genome, watched_gid = nets[best_alive_index]
            watching_label = "best genome" if watched_gid == best_genome_id else \
                             f"next best (fit={int(watched_genome.fitness or 0)})"

            panel_x, panel_y, panel_w, panel_h = 10, SCREEN_HEIGHT - 175, 430, 165
            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel.fill((240, 240, 240, 210))
            master.screen.blit(panel, (panel_x, panel_y))
            pygame.draw.rect(master.screen, (180, 180, 180),
                             (panel_x, panel_y, panel_w, panel_h), 1)

            def row(text, y_off, color=BLACK):
                master.screen.blit(font_mono.render(text, True, color),
                                   (panel_x + 8, panel_y + y_off))

            row(f"── {watching_label} ──────────────────",  6,  (100, 100, 100))
            row(f"Obstacle : {obs_desc}",                   26)
            row(f"Inputs   : DIST1={inputs[0]:.2f} TYPE1={inputs[1]:.1f} SIZE1={inputs[2]:.2f}", 46)
            row(f"           DINO_Y={inputs[3]:.2f} SPEED={inputs[4]:.2f}", 62)
            row(f"Outputs  : run={output[0]:.2f}  "
                f"jump={output[1]:.2f}  "
                f"duck={output[2]:.2f}",                    78)
            action_col = [BLACK, (30, 120, 200), (200, 130, 30)][action]
            row(f"Action   : {action_lbl}",                96, action_col)
            row(f"State    : jumping={bool(best_dino.is_jumping)}  "
                f"ducking={bool(best_dino.is_ducking)}",   112)
            row(f"Fitness  : {int(watched_genome.fitness or 0)}", 128, (100, 100, 100))

            pygame.draw.rect(master.screen, (255, 0, 0),   best_dino.get_rect(), 1)
            if nearest:
                pygame.draw.rect(master.screen, (0, 0, 255), nearest.get_rect(), 1)

        pygame.display.flip()
        clock.tick(0 if fast_mode else FPS)

    print(f"All dinos dead. Final score: {master.score // 10}")

if __name__ == "__main__":
    replay()