import neat
import pickle
import numpy as np
import pygame
from game import DinoGame, Dino, GROUND_Y, DINO_H

def eval_best_genome():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    try:
        with open("best_genome.pkl", "rb") as f:
            genome = pickle.load(f)
    except FileNotFoundError:
        print("No best_genome.pkl found.")
        return

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # Initialize headless game
    game = DinoGame(render=False)
    # Give it the hardest curriculum config (which spawns all obstacle types randomly)
    game.curriculum_gen = 100 
    
    # We will simulate high speeds
    game.reset()
    # game.speed = 15

    
    score = 0
    done = False
    
    print("Evaluating best_genome.pkl headlessly...")
    
    while not done and score < 50000:
        dino = game.dino
        
        master_state = game.get_state()
        
        ground_y   = GROUND_Y - DINO_H
        jump_phase = 0 if not dino.is_jumping else min(int((ground_y - dino.y) // 20), 3)

        inputs = (
            master_state[0] / 11.0,   # dist_bucket obstacle 1
            float(master_state[1]),   # obs_type1
            master_state[2],          # bird_y_norm1
            float(dino.is_jumping),   # dino's jump state
            jump_phase / 3.0,         # dino's jump phase
            float(dino.is_ducking),   # dino's duck state
        )

        output = net.activate(inputs)
        action = int(np.argmax(output))

        _, _, done = game.step(action)
        score += 1
        
        if score % 10000 == 0:
            print(f"Reached {score} frames. Current speed: {game.speed}")

    with open("eval.log", "w") as f:
        f.write(f"Evaluation complete. Survived for {score} frames. Speed reached: {game.speed}\n")
        if score >= 50000:
            f.write("Verdict: FULLY TRAINED!\n")
        else:
            f.write("Verdict: NOT FULLY TRAINED (Failed early).\n")

if __name__ == "__main__":
    eval_best_genome()
