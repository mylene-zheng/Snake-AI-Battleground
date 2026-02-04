# Snake AI: A* Pathfinding vs. Reinforcement Learning

This project is a comparative study of two artificial intelligence paradigms applied to the classic game "Snake": **Heuristic Planning (A*)** and **Autonomous Learning (Q-Learning)**. [cite_start]Developed as part of the Licence 3 Informatique at Université de Picardie Jules Verne[cite: 18, 20].

## 🧠 The Agents

- [cite_start]**A* Agent:** Uses the **Manhattan Distance** heuristic to calculate the shortest path to the target in real-time[cite: 119, 134]. It includes a survival "fallback strategy" for when paths are blocked[cite: 121].
- **RL Agent:** Implements **Q-Learning** with a discrete state space (Danger, Direction) and an **$\epsilon$-Greedy** exploration strategy[cite: 147, 157].

## 🏗️ Architecture
The system follows a strict **Agent-Environment** pattern to ensure modularity[cite: 29].

- **Noyau (Core):** A Python engine using `collections.deque` for $O(1)$ snake movement[cite: 108, 109].
- **Orchestrator:** Manages the 33ms/frame simulation loop and data flow between the AI and the world[cite: 37, 353].
- **Interface:** A Pygame-based GUI featuring a "Dark Mode" (Blue Night theme) and real-time KPI dashboard[cite: 192, 194].


## 📊 Key Performance Indicators (KPIs)
The application tracks several metrics to compare the two approaches[cite: 173]:
* [cite_start]**M-01: Optimality** – Ratio between path taken and theoretical minimum[cite: 176].
* [cite_start]**M-02: Execution Time** – CPU time per decision in ms[cite: 176].
* [cite_start]**M-03: Exploration Cost** – Number of nodes opened (A*)[cite: 176].
* [cite_start]**M-04: Memory** – RAM usage of the Q-Table or OpenSet[cite: 176].

## 🛠️ Installation & Usage

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/Snake-AI-Battleground.git](https://github.com/your-username/Snake-AI-Battleground.git)