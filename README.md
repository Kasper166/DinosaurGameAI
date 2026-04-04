# Dinosaur Game AI 🦖 🤖

A custom Pygame clone of the classic Chrome Dinosaur game played entirely by a neural network, trained from scratch using the **NeuroEvolution of Augmenting Topologies (NEAT)** algorithm.

![Demo GIF](demo.gif)

## 📌 Project Overview
The goal of this project is to develop an AI that can survive indefinitely in the game. The AI controls a dinosaur and must choose to either **Run, Jump, or Duck** at each frame to avoid upcoming obstacles (cacti or birds flying at different heights). 

Through thousands of simulated games and genetic evolution, the neural network learns to interpret the pixel distances and heights perfectly, successfully clearing obstacles at any game speed.

## 🧠 How the AI Works

### The Neural Network Inputs & Outputs
Each agent is powered by a feed-forward neural network. Every frame, the game environment feeds the network **9 inputs**:
- The distance bucket to the nearest obstacle.
- The type of the nearest obstacle (Bird vs. Cactus).
- The normalized Y-height of the bird (if applicable).
- The dinosaur's current physical state (whether it is currently jumping or ducking).
- The specific phase/height of the dinosaur's jump.
- Information about the next upcoming obstacle.

The network then calculates the probabilities and activates one of **3 outputs**:
- **0**: Do nothing (Run)
- **1**: Jump
- **2**: Duck

### Training with NEAT
The AI was trained using the `neat-python` library with a population size of 450 per generation.
- **Fitness:** Evaluated simply by how many frames an agent survives without dying.
- **Natural Selection:** The worst-performing neural networks are eliminated, while the best reproduce and mutate to form the next generation.
- **Dynamic Curriculum Learning:** To prevent the AI from adopting a lazy strategy of "always jumping" and failing to bird obstacles, the environment actively manipulates obstacle heights during early generations. Low/Mid birds are spawned early on to explicitly teach the network when to duck.

## 🚀 Running the Project Locally

### Requirements
- Python 3.10+
- `pygame`
- `neat-python`
- `numpy`
- `matplotlib` (for training visualization)

### Play the Game (Human Mode)
Want to try it yourself before watching the AI?
```bash
python game.py
```
*(Use `UP`/`SPACE` to jump and `DOWN` to duck)*

### Watch the Trained AI
To load the fully trained best genome (`best_genome.pkl`) and watch it play flawlessly:
```bash
python replay.py
```
*(Press `F` to enable Fast Mode and `D` to toggle the neural network's live Debug overlay!)*

### Train Your Own AI
Launch the training dashboard to start an evolutionary process from scratch:
```bash
python neat_train.py
```
A live `matplotlib` dashboard will open showing fitness graphs and tables for real-time tracking!

## 🔧 Built With
* [Python 3](https://www.python.org/)
* [Pygame](https://www.pygame.org/)
* [NEAT-Python](https://neat-python.readthedocs.io/en/latest/)

---
*Created as a portfolio piece showing competency in applying Reinforcement Learning principles, Neural Networks, and evolutionary algorithms to classical control environments.*
