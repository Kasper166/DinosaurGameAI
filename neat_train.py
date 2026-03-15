import neat
import pickle
from networkx import config
import pygame
from game import DinoGame, Dino
import numpy as np

def eval_genome(genome, config):
    """Run one genome (network) and return its fitness score."""
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = DinoGame(render=False)
    state = game.reset()
    done = False
    duck_count = 0
    jump_count = 0
    frames = 0

    while not done:
        # state is (dist_bucket, obs_type, is_jumping, jump_phase)
        # normalize inputs to roughly 0-1 range
        inputs = (
            state[0] / 11.0,   # dist_bucket
            state[1] / 2.0,    # obs_type
            float(state[2]),   # is_jumping
            state[3] / 3.0,    # jump_phase
        )
        output = net.activate(inputs)
        action = int(np.argmax(output))

        
        
        state, reward, done = game.step(action)
        frames += 1
    
    
    return frames
      # fitness = frames survived


def eval_genomes(genomes, config):
    best = None
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)
        if best is None or genome.fitness > best.fitness:
            best = genome

    # save best genome
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(best, f)
    
    # save all genomes of this generation
    with open("last_generation.pkl", "wb") as f:
        pickle.dump(genomes, f)

def run():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

   
    population = neat.Population(config)
   # reporters show progress in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.add_reporter(neat.Checkpointer(10))

    # run for up to 100 generations
    winner = population.run(eval_genomes, 500)
    plot_stats(stats) 

    # save the best genome
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Best genome saved.")

import matplotlib.pyplot as plt

def plot_stats(stats):
    generations = range(len(stats.most_fit_genomes))
    best_fitness = [g.fitness for g in stats.most_fit_genomes]
    avg_fitness = stats.get_fitness_mean()

    plt.figure(figsize=(10, 5))
    plt.plot(generations, best_fitness, label="Best fitness")
    plt.plot(generations, avg_fitness, label="Average fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (frames survived)")
    plt.title("NEAT Training Progress")
    plt.legend()
    plt.grid(True)
    plt.savefig("training_progress.png")
    plt.show()

if __name__ == "__main__":
    run()