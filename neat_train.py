import neat
import pickle
import pygame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from game import DinoGame, Dino

# ── Live dashboard setup ───────────────────────────────────────────────────────
fig = None
ax_fitness = None
ax_table = None
history = []  # list of dicts per generation
current_generation = 0 
def init_dashboard():
    global fig, ax_fitness, ax_table
    plt.ion()
    fig = plt.figure(figsize=(13, 6))
    fig.patch.set_facecolor('#f9f9f9')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.6, 1], figure=fig)
    ax_fitness = fig.add_subplot(gs[0])
    ax_table   = fig.add_subplot(gs[1])
    ax_table.axis('off')
    fig.suptitle('NEAT Training — Dino Game', fontsize=13, fontweight='bold', color='#222')
    plt.tight_layout(pad=2.0)

def update_dashboard(generation, best_fitness, avg_fitness, num_species):
    history.append({
        'gen':     generation,
        'best':    best_fitness,
        'avg':     avg_fitness,
        'species': num_species,
    })

    gens  = [h['gen']     for h in history]
    bests = [h['best']    for h in history]
    avgs  = [h['avg']     for h in history]

    # ── Left: fitness chart ────────────────────────────────────────────────────
    ax_fitness.clear()
    ax_fitness.plot(gens, bests, color='#3266ad', linewidth=2,   label='Best fitness',    marker='o', markersize=3)
    ax_fitness.plot(gens, avgs,  color='#888780', linewidth=1.5, label='Average fitness', marker='o', markersize=2, linestyle='--')
    ax_fitness.fill_between(gens, avgs, bests, alpha=0.08, color='#3266ad')
    ax_fitness.set_xlabel('Generation', fontsize=10, color='#555')
    ax_fitness.set_ylabel('Fitness (frames survived)', fontsize=10, color='#555')
    ax_fitness.set_title('Fitness over generations', fontsize=11, color='#333')
    ax_fitness.legend(fontsize=9)
    ax_fitness.grid(True, linestyle='--', alpha=0.4)
    ax_fitness.set_facecolor('#ffffff')
    ax_fitness.tick_params(labelsize=9)

    # ── Right: generation table ────────────────────────────────────────────────
    ax_table.clear()
    ax_table.axis('off')

    col_labels = ['Gen', 'Best', 'Avg', 'Species', 'Δ Best']
    all_time_best = max(bests)

    # show last 15 rows so the table doesn't overflow
    rows_to_show = history[-15:]
    table_data = []
    for i, row in enumerate(rows_to_show):
        actual_index = history.index(row)
        prev_best = history[actual_index - 1]['best'] if actual_index > 0 else None
        delta = f"+{int(row['best'] - prev_best)}" if prev_best is not None else '—'
        is_best = row['best'] == all_time_best
        marker = ' ★' if is_best else ''
        table_data.append([
            str(row['gen']),
            str(int(row['best'])) + marker,
            str(int(row['avg'])),
            str(row['species']),
            delta,
        ])

    

    # rebuild manually for full control
    
    tbl = ax_table.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc='center',
        loc='upper center',
        bbox=[0, 0, 1, 1]
    )

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)

    # style header row
    for col in range(len(col_labels)):
        cell = tbl[0, col]
        cell.set_facecolor('#3266ad')
        cell.set_text_props(color='white', fontweight='bold')

    # style data rows — highlight the all-time best row
    for row_i, row in enumerate(rows_to_show):
        for col in range(len(col_labels)):
            cell = tbl[row_i + 1, col]
            if row['best'] == all_time_best:
                cell.set_facecolor('#e8f0fb')
                cell.set_text_props(color='#1a3a6b', fontweight='bold')
            elif (row_i + 1) % 2 == 0:
                cell.set_facecolor('#f4f4f4')
            else:
                cell.set_facecolor('#ffffff')
            cell.set_edgecolor('#dddddd')

    ax_table.set_title(f'Last {len(rows_to_show)} generations', fontsize=10, color='#333', pad=6)

    plt.tight_layout(pad=2.0)
    plt.pause(0.001)


# ── NEAT evaluation ────────────────────────────────────────────────────────────
def eval_genome(genome, config, generation=0):
    net  = neat.nn.FeedForwardNetwork.create(genome, config)
    game = DinoGame(render=False)
    game.curriculum_gen = generation
    state = game.reset()
    done = False
    frames = 0

    while not done:
        inputs = (
            state[0] / 11.0,   # dist_bucket obstacle 1
            float(state[1]),   # obs_type1
            state[2],          # bird_y_norm1
            float(state[3]),   # is_jumping
            state[4] / 3.0,    # jump_phase
            float(state[5]),   # is_ducking
        )
        output = net.activate(inputs)
        action = int(np.argmax(output))
        state, reward, done = game.step(action)
        frames += 1

        if frames >= 20000:
            done = True

    return frames

def eval_genomes(genomes, config):
    best = None
    fitnesses = []
    global current_generation 

    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config, generation=current_generation)
        fitnesses.append(genome.fitness)
        if best is None or genome.fitness > best.fitness:
            best = genome

    # save best genome of this generation
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(best, f)
    with open("last_generation.pkl", "wb") as f:
        pickle.dump(genomes, f)

    # update live dashboard
    
    best_fit    = max(fitnesses)
    avg_fit     = sum(fitnesses) / len(fitnesses)
    num_species = len(config.species_set.species) if hasattr(config, 'species_set') else 0
    update_dashboard(current_generation+1, best_fit, avg_fit, num_species)

    current_generation += 1

# ── Run ────────────────────────────────────────────────────────────────────────
def run():
    global population
    cfg = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    init_dashboard()

    import os
    if os.path.exists("neat-checkpoint-20"):
        print("Resuming from checkpoint 20...")
        population = neat.Checkpointer.restore_checkpoint("neat-checkpoint-20")
    elif os.path.exists("neat-checkpoint-10"):
        print("Resuming from checkpoint 10...")
        population = neat.Checkpointer.restore_checkpoint("neat-checkpoint-10")
    else:
        population = neat.Population(cfg)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(10))

    winner = population.run(eval_genomes, 500)

    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Best genome saved.")

    # keep the final plot open
    plt.ioff()
    plt.savefig("training_progress.png", dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    run()