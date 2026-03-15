import neat
import pickle
import visualize  # neat's built-in helper


config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    "neat_config.txt"
)

with open("best_genome.pkl", "rb") as f:
    winner = pickle.load(f)

visualize.draw_net(config, winner, view=True, filename="network")


