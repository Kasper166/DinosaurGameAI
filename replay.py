import neat
import pickle
import numpy as np
import pygame
from game import DinoGame, Dino, GROUND_Y, DINO_H, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREY, FPS, draw_pixel_art, DINO_PIXELS_RUN1, DINO_PIXELS_RUN2

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

    # create a network for each genome
    nets = [(neat.nn.FeedForwardNetwork.create(genome, config), genome) for _, genome in genomes]

    # use one shared game for obstacles/speed but track each dino separately
    game = DinoGame(render=True)
    state = game.reset()

    # create a dino for each genome
    dinos = [Dino() for _ in range(len(nets))]
    alive = [True] * len(nets)

    clock = pygame.time.Clock()

    while any(alive):
        game.handle_quit()

        for i, (net, genome) in enumerate(nets):
            if not alive[i]:
                continue

            dino = dinos[i]

            # get state for this dino
            inputs = (
                state[0] / 11.0,
                state[1] / 2.0,
                float(dino.is_jumping),
                float(min(int((GROUND_Y - DINO_H - dino.y) // 20), 3)) / 3.0,
            )
            output = net.activate(inputs)
            action = int(np.argmax(output))

            if action == 1:
                dino.jump()
            elif action == 2:
                dino.duck(True)
            else:
                dino.duck(False)

            dino.update()

            # check collision for this dino
            for obs in game.obstacles:
                if dino.get_rect().colliderect(obs.get_rect()):
                    alive[i] = False
                    break

        # step the shared game (moves obstacles, updates score/speed)
        state, _, _ = game.step(0)  # action 0 = do nothing for the main game dino

        # draw everything manually
        game.screen.fill(WHITE)
        pygame.draw.line(game.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        for obs in game.obstacles:
            obs.draw(game.screen)

        # draw all alive dinos
        alive_count = sum(alive)
        for i, dino in enumerate(dinos):
            if alive[i]:
                dino.draw(game.screen)

        # show score and alive count
        font = pygame.font.SysFont(None, 36)
        game.screen.blit(font.render(f"Score: {game.score // 10}", True, BLACK), (SCREEN_WIDTH - 160, 20))
        game.screen.blit(font.render(f"Alive: {alive_count}/{len(nets)}", True, GREY), (SCREEN_WIDTH - 160, 60))

        pygame.display.flip()
        clock.tick(FPS)

    print(f"All dinos dead. Final score: {game.score}")

if __name__ == "__main__":
    replay()