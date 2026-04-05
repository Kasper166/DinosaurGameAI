import neat
import pickle
import pygame
import numpy as np
import json
import os
import matplotlib
matplotlib.use('Agg') # Headless mode: saves images without popping up windows
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
    # plt.ion()  # Removed to prevent pop-ups
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
    plt.savefig("training_progress.png", dpi=150, bbox_inches='tight')
    # plt.pause(0.001) # Removed to prevent pop-ups


# ── Training history helpers ──────────────────────────────────────────────────
HISTORY_FILE = "training_history.json"

def _load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def _save_history(hist):
    with open(HISTORY_FILE, "w") as f:
        json.dump(hist, f, indent=2)


# ── NEAT evaluation ────────────────────────────────────────────────────────────
def eval_genome(genome, config, generation=0):
    net  = neat.nn.FeedForwardNetwork.create(genome, config)
    game = DinoGame(render=False)
    game.use_score_curve = False   # keep curriculum for training
    game.curriculum_gen  = generation
    state = game.reset()
    done  = False
    frames = 0
    while not done:
        inputs = state # The state tuple has 10 values
        output = net.activate(inputs)
        action = int(np.argmax(output))
        state, _, done = game.step(action)
        frames += 1

        if frames >= 100000:
            done = True

    return frames

def eval_genomes(genomes, config):
    best      = None
    fitnesses = []
    global current_generation

    import random
    import numpy as np
    
    for genome_id, genome in genomes:
        # Fixed seeding for the entire generation ensures fairness
        random.seed(current_generation)
        np.random.seed(current_generation)
        
        genome.fitness = eval_genome(genome, config, generation=current_generation)
        fitnesses.append(genome.fitness)
        if best is None or genome.fitness > best.fitness:
            best = genome

    best_fit    = max(fitnesses)
    avg_fit     = sum(fitnesses) / len(fitnesses)
    num_species = len(config.species_set.species) if hasattr(config, 'species_set') else 0
    gen_number  = current_generation + 1

    # ── Persist best genome ────────────────────────────────────────────────────
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(best, f)
    with open("last_generation.pkl", "wb") as f:
        pickle.dump(genomes, f)

    # ── Write metadata for analytics screen ───────────────────────────────────
    with open("best_genome_meta.json", "w") as f:
        json.dump({"generation": gen_number, "fitness": int(best_fit)}, f)

    hist = _load_history()
    hist.append({
        "gen":     gen_number,
        "best":    int(best_fit),
        "avg":     int(avg_fit),
        "species": num_species,
    })
    _save_history(hist)

    # ── Update live matplotlib dashboard ──────────────────────────────────────
    update_dashboard(gen_number, best_fit, avg_fit, num_species)

    current_generation += 1
    
    # ── Custom termination: Average score >= 2000 ─────────────────────────────
    if avg_fit >= 5000:
        print(f"\n[SUCCESS] Goal Reached! Average score {int(avg_fit/10)} >= 2000.")
        print("Saving final results and stopping training...")
        plt.ioff()
        plt.savefig("training_progress.png", dpi=150, bbox_inches='tight')
        import sys
        sys.exit(0)

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

    # ── Reset / Start from Scratch ──────────────────────────────────────────
    # This ensures every training session starts fresh and overwrites old files.
    import glob
    files_to_delete = [
        "training_history.json", 
        "best_genome.pkl", 
        "best_genome_meta.json", 
        "last_generation.pkl"
    ]
    for f in files_to_delete:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass
            
    # Also delete legacy checkpoints
    for f in glob.glob("neat-checkpoint-*"):
        try: os.remove(f)
        except: pass
        
    print("[INIT] Old training data cleared. Starting fresh.")
    
    # Initialize fresh population
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
    # plt.show() # Removed to prevent pop-ups

if __name__ == "__main__":
    run()