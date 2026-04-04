"""
main.py — Pygbag async entry point for the browser build.

Run locally:   python -m pygbag main.py
Build for web: python -m pygbag --build main.py

The AI modes (Best Genome, Spectator) are desktop-only because
neat-python / numpy have no guaranteed WASM wheels.
This file exposes the human-play game loop via asyncio so Pygbag
can yield control to the browser's event loop each frame.
"""

import asyncio
import sys
import os

import pygame

# ── Shared game constants & classes from game.py ─────────────────────────────
from game import (
    DinoGame, Dino, show_analytics_screen,
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, DINO_H, FPS,
    WHITE, BLACK, GREY, BLUE,
    DINO_PIXELS_RUN1, DINO_PIXELS_RUN2, draw_pixel_art,
    PIXEL_SIZE,
)

# Detect web environment (Pygbag sets sys.platform to 'emscripten')
IS_WEB = sys.platform in ("emscripten", "wasm32")


# ── Game-state machine ────────────────────────────────────────────────────────
STATE_MENU    = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"


class WebGame:
    """Wraps DinoGame for single-loop async usage."""

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font_title = pygame.font.SysFont(None, 52)
        self.font_sub   = pygame.font.SysFont(None, 30)
        self.font_sm    = pygame.font.SysFont(None, 24)
        self.state      = STATE_MENU
        self.game       = None
        self.anim_tick  = 0
        self.dino_frame = 0

    # ── MENU ──────────────────────────────────────────────────────────────────
    def _draw_menu(self):
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK,
                         (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        grid = DINO_PIXELS_RUN1 if self.dino_frame == 0 else DINO_PIXELS_RUN2
        draw_pixel_art(self.screen, grid, 80, GROUND_Y - DINO_H, (83, 83, 83))

        title = self.font_title.render("DINOSAUR   AI", True, BLACK)
        self.screen.blit(title,
            (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        sub = self.font_sub.render("NEAT-powered evolution", True, GREY)
        self.screen.blit(sub,
            (SCREEN_WIDTH // 2 - sub.get_width() // 2, 82))

        opts = [
            ("[SPACE / TAP]  Play",    BLACK, 148),
            ("[↑] Jump   [↓] Duck",    GREY,  182),
        ]
        if IS_WEB:
            web_note = self.font_sm.render(
                "Browser build — AI modes available in the desktop version",
                True, (180, 120, 50))
            self.screen.blit(web_note,
                (SCREEN_WIDTH // 2 - web_note.get_width() // 2, 220))

        for label, color, y in opts:
            surf = self.font_sub.render(label, True, color)
            self.screen.blit(surf,
                (SCREEN_WIDTH // 2 - surf.get_width() // 2, y))

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                self._start_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._start_game()

    # ── PLAY ──────────────────────────────────────────────────────────────────
    def _start_game(self):
        self.game = DinoGame(render=False)  # we draw manually via self.screen
        self.game.screen = self.screen
        self.game.clock  = self.clock
        self.game.use_score_curve = True
        self.game.reset()
        self.state = STATE_PLAYING

    def handle_play_event(self, event):
        pass  # key state checked in tick

    def tick_play(self):
        keys   = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2

        # Touch / mouse support for web
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not keys[pygame.K_DOWN]:
            action = 1

        _, _, done = self.game.step(action)

        # Draw
        self.screen.fill(WHITE)
        pygame.draw.line(self.screen, BLACK,
                         (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        self.game.dino.draw(self.screen)
        for obs in self.game.obstacles:
            obs.draw(self.screen)
        score_text = self.game.font.render(
            f"Score: {self.game.score // 10:05d}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 175, 20))
        spd = self.font_sm.render(
            f"Speed: {self.game.speed:.1f}", True, GREY)
        self.screen.blit(spd, (10, 16))

        if done:
            self.state = STATE_GAMEOVER

    # ── GAME OVER ─────────────────────────────────────────────────────────────
    def _draw_gameover(self):
        """Simple blocking-free game-over panel (async-safe)."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))

        go = self.font_title.render("GAME  OVER", True, BLACK)
        self.screen.blit(go,
            (SCREEN_WIDTH // 2 - go.get_width() // 2, 60))

        ps = self.font_sub.render(
            f"Score: {self.game.score // 10:,}", True, BLACK)
        self.screen.blit(ps,
            (SCREEN_WIDTH // 2 - ps.get_width() // 2, 130))

        hint = self.font_sm.render(
            "[SPACE / TAP] Restart   [ESC] Menu", True, GREY)
        self.screen.blit(hint,
            (SCREEN_WIDTH // 2 - hint.get_width() // 2, 172))

    def handle_gameover_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._start_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._start_game()

    # ── Main tick ─────────────────────────────────────────────────────────────
    def tick(self, events):
        self.anim_tick += 1
        if self.anim_tick >= 8:
            self.anim_tick  = 0
            self.dino_frame = 1 - self.dino_frame

        for event in events:
            if event.type == pygame.QUIT:
                return False  # signal exit
            if self.state == STATE_MENU:
                self.handle_menu_event(event)
            elif self.state == STATE_PLAYING:
                self.handle_play_event(event)
            elif self.state == STATE_GAMEOVER:
                self.handle_gameover_event(event)

        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAYING:
            self.tick_play()
        elif self.state == STATE_GAMEOVER:
            self.tick_play.__func__  # keep last frame visible
            self._draw_gameover()

        return True  # keep running


# ── Async main loop (Pygbag entry point) ─────────────────────────────────────
async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dinosaur AI")
    clock = pygame.time.Clock()

    wgame = WebGame(screen, clock)

    running = True
    while running:
        events = pygame.event.get()

        # Quit shortcut
        for ev in events:
            if ev.type == pygame.QUIT:
                running = False

        if running:
            running = wgame.tick(events)
            pygame.display.flip()
            clock.tick(FPS)

        # Yield to browser
        await asyncio.sleep(0)

    pygame.quit()


# ── Desktop fallback (no Pygbag) ─────────────────────────────────────────────
if __name__ == "__main__":
    if IS_WEB:
        asyncio.run(main())
    else:
        # On desktop, launch the full-featured menu from game.py instead
        from game import main_menu
        main_menu()
