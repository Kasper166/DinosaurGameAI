import neat
import pickle
import numpy as np
import pygame
import imageio
from game import DinoGame, Dino, GROUND_Y, DINO_H

def record_demo():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    with open("best_genome.pkl", "rb") as f:
        genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Render True so we draw elements
    game = DinoGame(render=False) # Headless surface works if we call render_frame
    game.curriculum_gen = 100
    game.reset()
    game.speed = 12 # start semi-fast to show interesting gameplay

    frames_img = []
    score = 0
    done = False
    
    # Fast forward a bit of setup to get past the initial empty screen
    for _ in range(30):
        game.step(0)
    
    print("Recording frames...")
    
    while not done and score < 1500: # Record a longer sequence
        inputs = game.get_state()
        output = net.activate(inputs)
        action = int(np.argmax(output))

        _, _, done = game.step(action)
        
        # Draw frame
        game.render_frame(debug=False)
        
        # Capture frame (append every other frame to keep size small)
        if score % 2 == 0:
            frame = pygame.surfarray.array3d(game.screen)
            # Pygame uses (width, height, color), imageio uses (height, width, color)
            frame = np.transpose(frame, (1, 0, 2))
            frames_img.append(frame)
        
        score += 1

    print("Saving GIF...")
    imageio.mimsave("demo.gif", frames_img, fps=30)
    print("demo.gif saved!")

if __name__ == "__main__":
    record_demo()
